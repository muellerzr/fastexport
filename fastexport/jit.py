# AUTOGENERATED! DO NOT EDIT! File to edit: 00_jit.ipynb (unless otherwise specified).

__all__ = ['JitMode']

# Cell
import torch
from fastcore.all import *
from fastai.basics import *
from fastai.learner import *

# Internal Cell
@patch
def requires_grad_(self:TensorBase, requires_grad=True):
    # Workaround https://github.com/pytorch/pytorch/issues/50219
    self.requires_grad = requires_grad
    return self

# Cell
mk_class('JitMode', **{o:o.lower() for o in ['Trace','Script']},
         doc="All possible export modes as attributes to get tab-completion and typo-proofing")

# Cell
#nbdev_comment _all_ = ['JitMode']

# Cell
@patch
def to_jit(self:Learner, fname='export.ts', mode=JitMode.Trace, device='cpu'):
    "Exports `learn.model` using `jit` with `mode` to `fname`"
    inp = self.dls.one_batch()[:self.dls.n_inp]
    if not isinstance(inp, tuple): inp = (inp,)
    self.model.eval()
    self.model.to(device)
    inp = to_device(inp, device)
    traced_model = getattr(torch.jit, mode)(self.model, inp)
    torch.jit.save(traced_model, fname)