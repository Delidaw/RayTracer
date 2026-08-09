import numpy as np
import matplotlib.pyplot as plt

def plot_training_history(history):
    """
    Plots the training history to verify loss convergence.
    Expects 'history' to be the object returned by model.fit().
    """
    history_dict = history.history
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Plot Data Losses (MSE)
    axes[0].plot(history_dict.get('mse_rmin', []), label='r_min MSE', color='blue')
    axes[0].plot(history_dict.get('loss', []), label='Total Loss', color='black', linestyle='--')
    axes[0].set_title('Data Loss Convergence')
    axes[0].set_xlabel('Epochs')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # 2. Plot Physics Losses
    if 'phys_r' in history_dict or 'phys_phi' in history_dict:
        if 'phys_r' in history_dict:
            axes[1].plot(history_dict['phys_r'], label='Physics r_min Loss', color='red')
        if 'phys_phi' in history_dict:
            axes[1].plot(history_dict['phys_phi'], label='Physics Angular Loss', color='orange')
        
        axes[1].set_title('Physics Constraints Convergence')
        axes[1].set_xlabel('Epochs')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
    else:
        axes[1].text(0.5, 0.5, "Physics losses not found in history.", 
                     ha='center', va='center', fontsize=12)
        axes[1].set_title('Physics Constraints Convergence')
        
    plt.tight_layout()
    plt.show()

def compare_robustness(pinn_model, baseline_model, rmin_scaler, M=1.0):
    """
    Compares the robustness of a PINN model vs a purely data-driven baseline model
    near the critical boundary (b in [5.0M, 5.4M]).
    """
    # Fine-grained test sweep
    b_sweep = np.linspace(5.0 * M, 5.4 * M, 200)
    
    # Create input feature matrix: column 0 is M, column 1 is b
    X_test = np.column_stack((np.full_like(b_sweep, M), b_sweep))
    
    # Predict using both models
    # Assuming the models return: (rmin_scaled, phi, alpha, captured)
    preds_pinn = pinn_model.predict(X_test)
    preds_base = baseline_model.predict(X_test)
    
    # Inverse transform r_min
    rmin_pinn = preds_pinn[0].flatten() * rmin_scaler.scale_ + rmin_scaler.mean_
    rmin_base = preds_base[0].flatten() * rmin_scaler.scale_ + rmin_scaler.mean_
    
    # Extract alpha (deflection angle)
    alpha_pinn = preds_pinn[2].flatten()
    alpha_base = preds_base[2].flatten()
    
    # ---------------- Plotting ---------------- #
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: r_min vs b
    axes[0].plot(b_sweep, rmin_base, label='Data-Driven Baseline', color='blue', linestyle='--')
    axes[0].plot(b_sweep, rmin_pinn, label='PINN Surrogate', color='red')
    
    # Physical boundary: r_min cannot be less than 2M for escaping rays
    axes[0].axhline(2.0 * M, color='black', linestyle=':', label='Event Horizon (2M)')
    axes[0].fill_between(b_sweep, 0, 2.0 * M, color='black', alpha=0.1)
    
    axes[0].set_title('Robustness Test: Radial Periapsis ($r_{min}$)')
    axes[0].set_xlabel('Impact Parameter $b$')
    axes[0].set_ylabel('$r_{min}$')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot 2: Deflection Angle vs b
    axes[1].plot(b_sweep, alpha_base, label='Data-Driven Baseline', color='blue', linestyle='--')
    axes[1].plot(b_sweep, alpha_pinn, label='PINN Surrogate', color='red')
    
    # Physical boundary: deflection angle shouldn't go negative for attractive gravity
    axes[1].axhline(0, color='black', linestyle=':', label='Zero Deflection')
    axes[1].fill_between(b_sweep, -np.pi, 0, color='black', alpha=0.1)
    
    axes[1].set_title('Robustness Test: Deflection Angle ($\\alpha$)')
    axes[1].set_xlabel('Impact Parameter $b$')
    axes[1].set_ylabel('Deflection Angle (rad)')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.suptitle("PINN vs. Data-Driven Model Near Critical Boundary", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Running evaluation demo with mock models...")
    
    # 1. Mock Training History
    class MockHistory:
        def __init__(self):
            epochs = np.arange(1, 51)
            self.history = {
                'loss': 10.0 * np.exp(-0.1 * epochs) + 0.1 * np.random.rand(50),
                'mse_rmin': 8.0 * np.exp(-0.12 * epochs) + 0.1 * np.random.rand(50),
                'phys_r': 5.0 * np.exp(-0.15 * epochs) + 0.05 * np.random.rand(50),
                'phys_phi': 3.0 * np.exp(-0.1 * epochs) + 0.05 * np.random.rand(50),
            }
            
    mock_history = MockHistory()
    plot_training_history(mock_history)
    
    # 2. Mock Models
    class MockScaler:
        def __init__(self):
            self.scale_ = np.array([1.0])
            self.mean_ = np.array([0.0])
            
    class MockBaselineModel:
        def predict(self, X):
            b = X[:, 1]
            # Baseline hallucinates and dips below 2M near the boundary
            rmin = 2.0 + (b - 5.0) * 2.5 - 0.5 * np.exp(-50*(b-5.196)**2)
            alpha = np.pi * (5.5 - b) - 0.5 * np.exp(-50*(b-5.196)**2)
            return [rmin.reshape(-1, 1), None, alpha.reshape(-1, 1), None]
            
    class MockPINNModel:
        def predict(self, X):
            b = X[:, 1]
            # PINN adheres strictly to physics, curves asymptotically
            rmin = 2.0 + 3.0 * np.log1p(np.maximum(b - 5.15, 0.001))
            alpha = 1.0 / (np.maximum(b - 5.18, 0.01) + 0.1)
            return [rmin.reshape(-1, 1), None, alpha.reshape(-1, 1), None]
            
    baseline = MockBaselineModel()
    pinn = MockPINNModel()
    scaler = MockScaler()
    
    compare_robustness(pinn, baseline, scaler, M=1.0)
