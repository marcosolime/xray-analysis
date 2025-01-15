import torch
import torch.nn as nn
import torch.optim as optim
from pdb import set_trace as stx

# Simplified networks
class CoarseNetwork(nn.Module):
    def __init__(self, input_dim=3, hidden_dim=256):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 4)  # Output: RGB + Density
        )
    
    def forward(self, x):
        return self.fc(x)

class FineNetwork(nn.Module):
    def __init__(self, input_dim=3, hidden_dim=256):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 4)  # Output: RGB + Density
        )
    
    def forward(self, x):
        return self.fc(x)

# Volume rendering function
def volume_rendering(raw, z_vals, rays_d):
    # Simulate density-to-weight conversion and color blending
    alpha = 1.0 - torch.exp(-raw[..., 3])  # Raw density to alpha
    weights = alpha * torch.cumprod(torch.cat([torch.ones((alpha.shape[0], 1)), 1.0 - alpha + 1e-10], dim=-1), dim=-1)[:, :-1]
    rgb_map = torch.sum(weights[..., None] * raw[..., :3], dim=-2)  # Combine weights and colors
    return rgb_map

#stx()
# Initialize networks, optimizer, and loss
coarse_net = CoarseNetwork()
fine_net = FineNetwork()
optimizer = optim.Adam(list(coarse_net.parameters()) + list(fine_net.parameters()), lr=1e-3)
loss_fn = nn.MSELoss()

# Example data
rays_o = torch.rand(1024, 3)  # Origin of rays
rays_d = torch.rand(1024, 3)  # Direction of rays
gt_color = torch.rand(1024, 3)  # Ground truth pixel colors

# Ray sampling
z_vals = torch.linspace(0, 1, 64).expand(1024, 64)  # Coarse sampling
points = rays_o[..., None, :] + rays_d[..., None, :] * z_vals[..., :, None]  # 3D points, shape: (1024, 64, 3)

# Forward pass through coarse network
raw_coarse = coarse_net(points.view(-1, 3)).view(1024, 64, 4)   # shape: (1024, 64, 4)
rgb_coarse = volume_rendering(raw_coarse, z_vals, rays_d)       # shape: (1024, 3)          for each ray, there are rgb values

# Importance sampling
with torch.no_grad():
    weights = torch.sum(raw_coarse[..., 3], dim=-1)  # Weights for sampling
    z_vals_fine = torch.sort(torch.cat([z_vals, z_vals + torch.rand_like(z_vals) * 0.1], dim=-1), dim=-1).values # shape: (1024, 128)
    points_fine = rays_o[..., None, :] + rays_d[..., None, :] * z_vals_fine[..., :, None]                        # shape: (1024, 128, 3)

# Forward pass through fine network
raw_fine = fine_net(points_fine.view(-1, 3)).view(1024, -1, 4)  # shape: (1024, 128, 4)
rgb_fine = volume_rendering(raw_fine, z_vals_fine, rays_d)      # shape: (1024, 3)

# Compute loss
loss = loss_fn(rgb_coarse, gt_color) + loss_fn(rgb_fine, gt_color)

# Backward pass and optimization
optimizer.zero_grad()
loss.backward()
optimizer.step()

print(f"Loss: {loss.item()}")
