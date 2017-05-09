import torch
from collections import OrderedDict


class VoxNet(torch.nn.Module):

    def __init__(self, num_classes=10, input_shape=(32, 32, 32),
                 weights_path=None,
                 load_body_weights=True,
                 load_head_weights=True):
        """
        VoxNet: A 3D Convolutional Neural Network for Real-Time Object Recognition.

        Modified in order to accept different input shapes.

        Parameters
        ----------
        num_classes: int, optional
            Default: 10
        input_shape: (x, y, z) tuple, optional
            Default: (32, 32, 32)
        weights_path: str or None, optional
            Default: None
        load_body_weights: bool, optional
            Default: True
        load_head_weights: bool, optional
            Default: True

        Notes
        -----
        Weights avaliable at: url to be added

        If you want to finetune with custom classes, set load_head_weights to False.
        Default head weights are pretrained with ModelNet10.
        """
        super().__init__()
        self.body = torch.nn.Sequential(OrderedDict([
            ('conv1', torch.nn.Conv3d(in_channels=1, out_channels=32, kernel_size=5, stride=2)),
            ('lkrelu1', torch.nn.LeakyReLU()),
            ('drop1', torch.nn.Dropout(p=0.2)),
            ('conv2', torch.nn.Conv3d(in_channels=32, out_channels=32, kernel_size=3)),
            ('lkrelu2', torch.nn.LeakyReLU()),
            ('pool2', torch.nn.MaxPool3d(2)),
            ('drop2', torch.nn.Dropout(p=0.3))
        ]))

        # Trick to accept different input shapes
        x = self.body(torch.autograd.Variable(torch.rand((1, 1) + input_shape)))
        first_fc_in_features = 1
        for n in x.size()[1:]:
            first_fc_in_features *= n

        self.head = torch.nn.Sequential(OrderedDict([
            ('fc1', torch.nn.Linear(first_fc_in_features, 128)),
            ('relu1', torch.nn.ReLU()),
            ('drop3', torch.nn.Dropout(p=0.4)),
            ('fc2', torch.nn.Linear(128, num_classes))
        ]))

        if weights_path is not None:
            weights = torch.load(weights_path)
            if load_body_weights:
                self.body.load_state_dict(weights["body"])
            elif load_head_weights:
                self.head.load_state_dict(weights["head"])

    def forward(self, x):
        x = self.body(x)
        x = x.view(x.size(0), -1)
        x = self.head(x)
        return x
