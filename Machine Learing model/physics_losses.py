import tensorflow as tf
import numpy as np

def rmin_pinn_loss(M=1.0, physics_weight=0.1):
    """
    Creates a Physics-Informed Neural Network (PINN) loss for the r_min model.
    
    The radial periapsis constraint for an escaping photon is:
    b^2 * (1 - 2M / r_min) - r_min^2 = 0
    
    Usage:
    Compile the model with this loss. Since Keras loss functions only accept
    (y_true, y_pred), you must stack the true r_min and the impact parameter 'b' 
    into your y_true array when preparing your training data.
    
    y_true_stacked = np.column_stack((y_true_rmin, b_values))
    model.compile(optimizer='adam', loss=rmin_pinn_loss(M=1.0, physics_weight=0.1))
    """
    def loss(y_true_stacked, y_pred):
        # Unpack y_true_stacked (assuming shape is [batch_size, 2])
        # Column 0: Actual r_min (ground truth from geodesic integration)
        # Column 1: Impact parameter (b)
        y_true = y_true_stacked[:, 0:1]
        b = y_true_stacked[:, 1:2]
        
        # 1. Standard Data Loss (Mean Squared Error)
        data_loss = tf.reduce_mean(tf.square(y_true - y_pred))
        
        # 2. Physics-Informed Loss
        # Constraint: b^2 * (1 - 2M / r_min) - r_min^2 = 0
        b_sq = tf.square(b)
        r_min_pred = y_pred
        r_min_sq = tf.square(r_min_pred)
        
        physics_constraint = b_sq * (1.0 - (2.0 * M) / (r_min_pred + 1e-7)) - r_min_sq
        physics_loss = tf.reduce_mean(tf.square(physics_constraint))
        
        # Combine both losses
        return data_loss + (physics_weight * physics_loss)
        
    return loss


def angular_consistency_loss(physics_weight=0.1):
    """
    Creates a geometric consistency loss for models predicting deflection angle (alpha) 
    and final azimuthal sweep (phi).
    
    The constraint is: alpha - (phi_final - phi_initial) + pi = 0
    
    Usage:
    y_true_stacked = np.column_stack((y_true_alpha, phi_final_values, phi_initial_values))
    model.compile(optimizer='adam', loss=angular_consistency_loss())
    """
    def loss(y_true_stacked, y_pred_alpha):
        # Unpack the inputs
        # Column 0: Actual alpha (deflection angle)
        # Column 1: phi_final
        # Column 2: phi_initial (usually 0)
        y_true = y_true_stacked[:, 0:1]
        phi_final = y_true_stacked[:, 1:2]
        phi_initial = y_true_stacked[:, 2:3]
        
        # 1. Standard Data Loss (MSE)
        data_loss = tf.reduce_mean(tf.square(y_true - y_pred_alpha))
        
        # 2. Physics Geometric Consistency Loss
        # alpha - (phi_final - phi_initial) + pi = 0
        pi = tf.constant(np.pi, dtype=tf.float32)
        delta_phi = phi_final - phi_initial
        
        physics_constraint = y_pred_alpha - delta_phi + pi
        physics_loss = tf.reduce_mean(tf.square(physics_constraint))
        
        # Combine both losses
        return data_loss + (physics_weight * physics_loss)
        
    return loss
