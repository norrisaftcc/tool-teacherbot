# Learn — Manning Ch 1 + Ch 4 framing

**Slot:** Learn (low-stakes, no submission)
**Time:** ~60 minutes including reading
**Goal:** Walk into [practice.md](practice.md) knowing what "training a neural network" actually means, even before you write a line of code.

---

## What to read

- **Manning Ch 1** — *What is deep learning?* Skim. Don't try to retain every detail. You want the shape: what AI is, where DL sits inside it, what's changed in the last few years, why generative AI is a big deal now.
- **Manning Ch 4 §1–2** — *Classification and regression.* This is the *frame* we'll use for the rest of the term. Almost every model you build will be one of these two shapes.

We don't lecture the textbook back at you. Meeting A is where you ask questions about what you read.

## The five things you need from this reading

If you only retain five things from Week 2's reading, retain these.

### 1. Deep learning is just "stack of layers + lots of data + gradient descent"

Strip the marketing. A neural network is a stack of mathematical operations (layers) with adjustable parameters (weights), trained by showing it lots of examples and nudging the weights to reduce error. The "deep" part means "many layers." That's the whole story at this altitude.

What's changed isn't the idea — it's that we now have enough data, enough compute, and enough engineering polish (Keras, PyTorch, JAX) to make this actually work for real problems.

### 2. Almost everything you'll build is **classification** or **regression**

| You're predicting... | It's a... | Output layer |
|---|---|---|
| ...a category (this image is a 7, this email is spam) | Classification | `softmax` (multi-class) or `sigmoid` (binary) |
| ...a continuous number (house price, temperature tomorrow) | Regression | Usually no activation on the output |

Image classification is classification. Sentiment analysis is classification. Object detection is classification (per region). Translation is classification (per token). Forecasting house prices is regression. Forecasting demand is regression.

This is reductive. It's also correct often enough that holding this frame in your head will save you a lot of confusion later.

### 3. The "universal workflow" — task → metric → baseline → improve

From Ch 4 (and we'll go deeper in Week 5 with Ch 6). Every project follows roughly:

1. **What's the task?** (Predict X given Y.)
2. **What's the metric?** (Accuracy? F1? RMSE? Decide *before* training.)
3. **Build a baseline.** A weak model that beats random. Often a one-line scikit-learn fit.
4. **Improve.** Try something. Measure. Try something else. Measure.

If you can answer 1 and 2 in one sentence each, you have a real project. If you can't, you have an idea, not a project.

### 4. Keras is the API; TensorFlow / JAX / PyTorch are the engines

Don't get confused on this. **Keras** is the high-level API you'll be writing this week — `Sequential`, `Dense`, `.fit()`, `.compile()`. Underneath, it can run on TensorFlow, JAX, or PyTorch (Manning 3e uses JAX-friendly Keras 3). For everything we do this week, the engine doesn't matter — you're writing Keras.

Why this matters: when you Google something and a Stack Overflow answer says "use `tf.keras.X`," ignore the `tf.` prefix. The Keras API is portable.

### 5. The system prompt is the product / the training loop is the product

Last week we said the system prompt is the most important engineering artifact when building agents. This week the equivalent is **the training loop** — the `.compile()` + `.fit()` calls with your loss function, optimizer, metrics, and callbacks. A vague training loop produces a vague model. We'll obsess about this for the next 7 weeks.

## The notebook you'll be referencing

The companion notebook for Ch 4 is at:

```
planning/textbook/deep-learning-with-python-notebooks-master/chapter04_classification-and-regression.ipynb
```

You don't have to run it before [practice.md](practice.md). But skim it. The Manning notebooks are the *primary source* for textbook code — we don't duplicate that code into our materials, we point at it.

## Two terms you'll hear all term

- **Epoch:** one pass through the entire training dataset. "Train for 5 epochs" means show the model each training example 5 times.
- **Batch:** the chunk of examples the model looks at before updating its weights. Common batch sizes: 32, 64, 128. (Why those numbers? Mostly historical. Powers of 2 used to matter for GPU memory; less so now.)

You'll also hear **learning rate**, **loss function**, **optimizer**. We'll handle those in Week 3 (Ch 2 — the math-for-debugging week). For Week 2, you can leave them at the defaults Manning Ch 4 gives you.

## Where to go next

→ [practice.md](practice.md) — Hello, training loop. Get the mechanics in your fingers.
