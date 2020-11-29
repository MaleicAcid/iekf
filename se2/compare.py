import numpy as np
import matplotlib.pyplot as plt

from system import UnicycleSystem
from iekf import InvariantEKF
from ekf import ExtendedKalmanFilter

 # setup system
Q = np.diag([.01, 0, .1])
R = np.diag([.001, .001])
dt = 0.1
sys = UnicycleSystem(Q, R, dt)
x0 = np.zeros(3)

# generate data from Lie Group method
t = 100
u = lambda t: np.array([1, 3*np.sin(t/2)])
u = np.array([u(t) for t in range(t)])
x, _, z = sys.gen_data(x0, u, t, noise=True)

#remove "1" from z
z = z[:,:2]


# Run the ekf
ekf = ExtendedKalmanFilter(sys, x0, np.eye(3))
mus_ekf, sigmas = ekf.iterate(u, z)

# Run the iekf
iekf = InvariantEKF(sys, x0, np.eye(3))
mus_iekf, sigmas = iekf.iterate(u, z)

# plot results
plt.plot(x[:,0,2], x[:,1,2], label="Actual Location")
plt.plot(z[:,0], z[:,1], label="Measurements", alpha=0.5)
plt.plot(mus_ekf[:,0], mus_ekf[:,1], label="EKF Results")
plt.plot(mus_iekf[:,0,2], mus_iekf[:,1,2], label="iEKF Results")
plt.legend()
plt.show()