# Practice — Hello, training loop

**Slot:** Practice (retry-OK, no grade penalty)
**Time:** ~75 minutes
**Goal:** Load MNIST through Keras, train a `Sequential` model, look at the loss curve. By the end you should be able to do this from scratch *without copying from this file.*

This lab is adapted from `planning/csc_dash/CSC-114/activities/Module_01_Sacred_Flow_Lab.md` — the environment-setup half is unchanged. The model-building half swaps **sklearn-Iris** for **Keras-MNIST**, because we're training neural networks now, not decision trees.

---

## Part 1 — Environment check (skip if already working)

You need Python 3.10+ with `jupyter`, `numpy`, `tensorflow` (or `jax` + `keras`), and `matplotlib`. If you already have a working `ml-env` from CSC-113 or another class, activate it, install `tensorflow`, and skip to Part 2.

If you're starting from scratch, the full environment-setup walkthrough is in `planning/csc_dash/CSC-114/activities/Module_01_Sacred_Flow_Lab.md` — **Parts 1 and 2** of that file are accurate for Week 2; we override only Part 3 (the actual model) here.

Add these to your install line:

```bash
pip install tensorflow  # or: pip install jax keras
```

Verify:

```bash
python -c "import keras; print(f'Keras version: {keras.__version__}')"
```

You should see Keras 3.x. If you see Keras 2.x with TensorFlow, that's fine — the code below works on both.

**If your laptop won't install TensorFlow** (Apple Silicon weirdness, Windows MSVC errors, etc.), use [Google Colab](https://colab.research.google.com) for this week and address local install separately. Don't fight your laptop on Day 8.

## Part 2 — Build, train, evaluate

Create a notebook called `week-02/hello_keras.ipynb`. The notebook should have these cells, in this order. Type them — don't copy. The point is muscle memory.

### Cell 1: Imports

```python
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras import layers

print(f"Keras: {keras.__version__}")
```

### Cell 2: Load MNIST

```python
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print(f"Training images: {x_train.shape}, labels: {y_train.shape}")
print(f"Test images:     {x_test.shape}, labels: {y_test.shape}")
print(f"Pixel value range: {x_train.min()} to {x_train.max()}")
```

You should see 60,000 training images of shape (28, 28), 10,000 test images, pixel values 0–255. **Look at the output.** Don't just run the cell.

### Cell 3: Look at the data

```python
fig, axes = plt.subplots(1, 5, figsize=(10, 2))
for i, ax in enumerate(axes):
    ax.imshow(x_train[i], cmap="gray")
    ax.set_title(f"Label: {y_train[i]}")
    ax.axis("off")
plt.show()
```

You'll see 5 handwritten digits with their labels. The model's job will be to predict those labels from the pixels.

### Cell 4: Preprocess

```python
x_train = x_train.reshape((60000, 28 * 28)).astype("float32") / 255.0
x_test  = x_test.reshape((10000, 28 * 28)).astype("float32") / 255.0

print(f"Reshaped training: {x_train.shape}, dtype: {x_train.dtype}")
print(f"Pixel value range after scaling: {x_train.min()} to {x_train.max()}")
```

Two things happened here. We flattened each 28×28 image into a 784-long vector (because our first model uses Dense layers, which expect 1D input — Week 6's CNNs will keep the 2D shape). And we scaled pixels to 0–1 because neural networks train much better on small input numbers.

### Cell 5: Build the model

```python
model = keras.Sequential([
    layers.Input(shape=(28 * 28,)),
    layers.Dense(128, activation="relu"),
    layers.Dense(10,  activation="softmax"),
])

model.summary()
```

Three things to notice in the summary:
- The model has **two layers** (the `Input` layer is a spec, not a layer with weights).
- The hidden layer has **100,480 trainable parameters** (= 784 × 128 + 128). The output layer adds 1,290. Total around 101,770.
- The shape going *out* of the network is `(None, 10)` — one number per class.

### Cell 6: Compile

```python
model.compile(
    optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
```

This is the line you'll obsess about all term. For now, accept the defaults: `rmsprop` is a reasonable optimizer, `sparse_categorical_crossentropy` is the right loss for "predict one of N classes when labels are integers," `accuracy` is the metric we want to watch.

### Cell 7: Train

```python
history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=128,
    validation_split=0.1,
)
```

You'll see five lines of output, one per epoch. The numbers that matter:
- `loss` and `val_loss` — training and validation loss.
- `accuracy` and `val_accuracy` — training and validation accuracy.

By epoch 5 you should be over **97% validation accuracy**. If you're way below that, something's wrong — re-check Cell 4 (the preprocessing).

### Cell 8: Look at the training curves

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(history.history["loss"],     label="train")
axes[0].plot(history.history["val_loss"], label="val")
axes[0].set_title("Loss"); axes[0].legend()
axes[1].plot(history.history["accuracy"],     label="train")
axes[1].plot(history.history["val_accuracy"], label="val")
axes[1].set_title("Accuracy"); axes[1].legend()
plt.show()
```

**Stare at this plot for a minute.** Are train and val curves close, or pulling apart? If they're pulling apart with train going up and val going flat/down, that's *overfitting* — Week 5's territory.

### Cell 9: Evaluate on test

```python
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")
```

Write this number down. It is your **baseline metric**. You'll use it in [apply.md](apply.md).

### Cell 10: Predict on one image

```python
import random
i = random.randint(0, len(x_test) - 1)
prediction = model.predict(x_test[i:i+1], verbose=0)
predicted_label = prediction.argmax()
true_label = y_test[i]

plt.imshow(x_test[i].reshape(28, 28), cmap="gray")
plt.title(f"Predicted: {predicted_label}  |  True: {true_label}")
plt.axis("off")
plt.show()
```

Run this cell a few times. Find one where the model is *wrong* — there will be some. Note what the misclassified digit looks like. We'll come back to this in [apply.md](apply.md).

## Part 3 — Reflection cell

Add a markdown cell at the bottom of your notebook:

```markdown
## Reflection

1. **What did this model do?**
   [Your answer.]

2. **What did the training curves show?**
   [Train/val gap? Plateau? Still improving at epoch 5?]

3. **Did the test accuracy match the validation accuracy?**
   [Should be close. If wildly different, something's off.]

4. **What would you try first if you wanted to improve this?**
   [Don't think hard. First instinct. We'll test it in apply.md.]
```

Save the notebook.

## Before you leave Practice

- [ ] Your notebook runs end-to-end without errors.
- [ ] You hit ~97%+ test accuracy.
- [ ] You can point at the training curves and say something about them.
- [ ] You wrote the reflection cell.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'keras'` | Wrong env or not installed | `pip install tensorflow` in the active venv. |
| Test accuracy around 10% (random) | Forgot to scale pixels to 0–1 in Cell 4 | Re-run Cell 4 with the `/ 255.0`. |
| `ValueError: ... shape ...` | Forgot the `.reshape((60000, 28*28))` in Cell 4 | Same fix. Dense layers want 1D input. |
| Training is **very** slow | Local CPU, or installed `tensorflow-gpu` without a GPU | Use Colab for this week. |
| `RuntimeError: ... mixed backends ...` (Keras 3) | Mixed JAX and TF | Set `KERAS_BACKEND` env var to one or the other before importing keras. |

## Where to go next

→ [apply.md](apply.md) — Your first spike prototype: pick one thing and improve on the baseline.
