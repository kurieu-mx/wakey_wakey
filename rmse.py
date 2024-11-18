import numpy as np
from sklearn.metrics import mean_squared_error

def rmse(y_true, y_pred):
    """Calculates the Root Mean Squared Error (RMSE) between true and predicted values."""
    return np.sqrt(mean_squared_error(y_true, y_pred))

y_true =[] #input from arduino
y_pred = [] 
rmse_value = rmse(y_true, y_pred)
print("RMSE:", rmse_value)