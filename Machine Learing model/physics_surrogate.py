import tensorflow as tf
from tensorflow.keras import models

class PhysicsInformedSurrogate(models.Model):
    def __init__(self, multitask_network, rmin_scaler, lambda_r=0.1, lambda_phi=0.05):
        super().__init__()
        self.network = multitask_network
        self.rmin_scaler = rmin_scaler
        self.lambda_r = lambda_r
        self.lambda_phi = lambda_phi

    def train_step(self, data):
        # Unpack input features and ground-truth targets
        x, y = data
        
        # Extract features (M at index 0, b at index 1)
        M_tensor = x[:, 0:1]
        b_tensor = x[:, 1:2]
        
        # Target vectors
        y_rmin = y["rmin"]
        y_phi = y["phi"]
        y_alpha = y["alpha"]
        y_captured = y["captured"]

        with tf.GradientTape() as tape:
            # 1. Forward Pass
            rmin_pred_scaled, phi_pred, alpha_pred, captured_pred = self.network(x, training=True)
            
            # Inverse-scale rmin prediction to physical space for computing physical equations
            rmin_pred = rmin_pred_scaled * self.rmin_scaler.scale_ + self.rmin_scaler.mean_
            
            # 2. Standard Data Losses (MSE / BCE)
            loss_rmin = tf.reduce_mean(tf.square(rmin_pred_scaled - y_rmin))
            loss_phi = tf.reduce_mean(tf.square(phi_pred - y_phi))
            loss_alpha = tf.reduce_mean(tf.square(alpha_pred - y_alpha))
            
            # Binary Cross Entropy for capture head
            loss_captured = tf.keras.losses.binary_crossentropy(y_captured, captured_pred)
            
            # 3. Physics Loss (only active for escaping trajectories where y_captured == 0)
            escape_mask = tf.cast(tf.equal(y_captured, 0), tf.float32)
            
            # Physics-Informed r_min loss
            r_phys_error = b_tensor**2 * (1.0 - (2.0 * M_tensor) / rmin_pred) - rmin_pred**2
            loss_phys_r = tf.reduce_mean(escape_mask * tf.square(r_phys_error))
            
            # Physics-Informed angle consistency loss (assuming phi_initial = pi)
            phi_init = 3.14159265
            loss_phys_phi = tf.reduce_mean(
                escape_mask * tf.square(alpha_pred - (phi_pred - phi_init) + 3.14159265)
            )
            
            # 4. Total Loss
            total_loss = (loss_rmin + loss_phi + loss_alpha + loss_captured + 
                          self.lambda_r * loss_phys_r + self.lambda_phi * loss_phys_phi)

        # 5. Backward Pass and Weight Update
        gradients = tape.gradient(total_loss, self.network.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.network.trainable_variables))
        
        return {
            "loss": total_loss, 
            "mse_rmin": loss_rmin, 
            "phys_r": loss_phys_r, 
            "phys_phi": loss_phys_phi
        }

    def call(self, inputs, training=False):
        return self.network(inputs, training=training)
