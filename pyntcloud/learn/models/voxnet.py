"""
Implementation of:

Maturana, D. and Scherer, S.;
VoxNet: A 3D Convolutional Neural Network for Real-Time Object Recognition.

Modified in order to accept different input shapes.
"""
import torch
from collections import OrderedDict


class VoxNet(torch.nn.Module):

    def __init__(self, num_classes=10, input_shape=(32, 32, 32)):

        super().__init__()
        self.body = torch.nn.Sequential(OrderedDict([
            ('conv1', torch.nn.Conv3d(in_channels=1, out_channels=32, kernel_size=5, stride=2)),
            ('lkrelu1', torch.nn.LeakyReLU()),
            ('drop1', torch.nn.Dropout(p=0.2)),
            ('conv2', torch.nn.Conv3d(in_channels=32, out_channels=32, kernel_size=3, stride=2)),
            ('lkrelu2', torch.nn.LeakyReLU()),
            ('pool2', torch.nn.MaxPool3d(2)),
            ('drop2', torch.nn.Dropout(p=0.3))
        ]))

        # Trick to accept different input shapes
        x = self.body(torch.autograd.Variable(torch.rand((1, 1) + input_shape)))
        first_fc_in_features = 1
        for n in x.size()[1:]:
            first_fc_in_features *= n

        self.head = torch.nn.Sequential(
            torch.nn.Linear(first_fc_in_features, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.4),
            torch.nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.body(x)
        x = x.view(x.size(0), -1)
        x = self.head(x)
        return x
