import torch
print(torch.cuda.is_available())   # Should be True
print(torch.cuda.device_count())   # Should be >= 1
print(torch.cuda.get_device_name(0))  # Should show "NVIDIA GeForce RTX 4050"