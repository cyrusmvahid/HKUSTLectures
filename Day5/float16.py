from typing import Any, Union

import mxnet as mx
import gluoncv as gcv
from mxnet import autograd, nd, metric, gluon
from mxnet.gluon.data.vision import transforms
import multiprocessing as mp
import time

print(mx.__version__)

from mxnet.ndarray import NDArray

MIXED_PRECISION = False
TYPECAST = 'float32'
if MIXED_PRECISION:
    TYPECAST = 'float16'

NAIVE = False
NUM_WORKERS = 1
if not NAIVE:
    NUM_WORKERS = mp.cpu_count() - 3

MULTI_GPU = True
NUM_GPU = 1
if MULTI_GPU:
    NUM_GPU = mx.context.num_gpus()

ctx = [mx.gpu(i) for i in range(NUM_GPU)]
BATCH_SIZE = 64 * NUM_GPU

SYMBOLIC=True


net = gcv.model_zoo.get_model(name='resnet50_v2', pretrained=False)

train_trans = transforms.Compose([transforms.RandomResizedCrop(size=(224, 224)), transforms.Cast(TYPECAST)])
train_dataset = gluon.data.vision.CIFAR100(train=True).transform_first(train_trans)
train_data = gluon.data.DataLoader(train_dataset, shuffle=True, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS, last_batch='discard')

test_trans = transforms.Compose([transforms.Resize(size=(224, 224)), transforms.Cast(TYPECAST)])
test_dataset = gluon.data.vision.CIFAR100(train=False).transform_first(test_trans)
test_data = gluon.data.DataLoader(test_dataset, shuffle=False, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS, last_batch='discard')
if SYMBOLIC:
    net.hybridize(static_alloc=True, static_shape=True)

net.cast(TYPECAST)
net.initialize(ctx=ctx, force_reinit=True)

optimizer = mx.optimizer.SGD(momentum=0.9, learning_rate=.001, multi_precision=True)
trainer = gluon.Trainer(params=net.collect_params(), optimizer=optimizer)
loss_fn = gluon.loss.SoftmaxCrossEntropyLoss()

metrics = metric.CompositeEvalMetric([metric.Accuracy(), metric.RMSE()])
epochs = 3
outputs = False
old_label = False
first_run = True
print_n_sync = 2


for e in range(epochs):
    metrics.reset()
    tick = time.time()
    etic = time.time()
    for i, minibatch in enumerate(train_data):
        if i == 0:
            tick_0 = time.time()


        data = gluon.utils.split_and_load(data=minibatch[0], ctx_list=ctx, batch_axis=0, even_split=True)
        label = gluon.utils.split_and_load(data=minibatch[1], ctx_list=ctx, batch_axis=0, even_split=True)

        old_label = label
        #if i % print_n_sync == 0 and i > 0 and not first_run:
        #    metrics.update(labels=old_label, preds=outputs)




        with autograd.record():
            outputs = [net(d) for d in data]
            loss = [loss_fn(yhat, y) for yhat, y in zip(outputs, label)]

        for l in loss:
            l.backward()

        trainer.step(batch_size=BATCH_SIZE)
        first_run = False


    print(e)
    tick = time.time()
    print("NUM_GPU: {}, NUM_WORKER: {}, BATCH_SIZE_PER_GPU: {}, TYPECAST: {}, SYMBOLIC: {}".format(NUM_GPU,
                                                                                     NUM_WORKERS,
                                                                                     BATCH_SIZE/NUM_GPU,
                                                                                     #type(outputs[0][0][0].asscalar())
                                                                                     TYPECAST,
                                                                                     SYMBOLIC))
    print('~Samples/Sec {:.4f}'.format(data[0].shape[0] * NUM_GPU * (i + 1) / (time.time() - tick_0)))
    #print(metrics.get_name_value())
    print('epoch time: {}'.format((time.time() - etic)))



