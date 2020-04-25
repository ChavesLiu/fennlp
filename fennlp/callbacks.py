#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:Kaiyin Zhou
"""

import numpy as np


class EarlyStopping:
    def __init__(self, monitor="loss",
                 min_delta=0,
                 patience=0,
                 mode='auto',
                 baseline=None,
                 restore_best_weights=True,
                 verbose=1):
        self.wait = 0
        self.min_delta = min_delta
        self.mode = mode
        self.patience = patience
        self.verbose = verbose
        self.monitor = monitor
        self.baseline = baseline
        self.restore_best_weights = restore_best_weights
        if mode not in ['auto', 'min', 'max']:
            print('EarlyStopping mode %s is unknown, '
                  'fallback to auto mode.', mode)
            mode = 'auto'
        if mode == 'min':
            self.monitor_op = np.less
        elif mode == 'max':
            self.monitor_op = np.greater
        else:
            if 'acc' in self.monitor:
                self.monitor_op = np.greater
            else:
                self.monitor_op = np.less

        if self.monitor_op == np.greater:
            self.min_delta *= 1
        else:
            self.min_delta *= -1

        if self.baseline is not None:
            self.best = self.baseline
        else:
            self.best = np.Inf if self.monitor_op == np.less else -np.Inf

    def __call__(self, current, model=None):
        if model == None:
            self.restore_best_weights = False
        if current is None:
            return True
        if self.monitor_op(current - self.min_delta, self.best):
            self.best = current
            self.wait = 0
            if self.restore_best_weights:
                self.best_weights = model.get_weights()
        else:
            self.wait += 1
            if self.wait >= self.patience:
                print('Early stopping ...')
                if self.restore_best_weights:
                    if self.verbose > 0:
                        print('Restoring model weights from the end of the best epoch.')
                    model.set_weights(self.best_weights)
                return True
