Quiz title: Week 2 Knowledge Check — Keras Hello World
Quiz description: Vocabulary check for Manning Ch 1 + Ch 4 and the two-track Sacred Flow workflow. Unlimited attempts; the goal is mastery, not test-taking. Read the explanations on anything you miss.


1.  What does it mean for a problem to be "supervised learning"?
*a) The training data includes both inputs and known correct outputs.
b)  A human watches the model as it trains.
c)  The model only works with labeled images.
d)  The model requires constant human intervention during inference.
... "Supervised" describes the data, not the process. You have examples with answers, and the model learns to map inputs to outputs by minimizing how often it gets those answers wrong. There's no human babysitting required during training — you set up the data and the loss function and let the optimizer do the work. The opposite, unsupervised learning, has no answer key, so the model has to find structure on its own.


2.  You're building a model to predict the price of a used car from its mileage, year, and make. What kind of problem is this?
a)  Classification — the categories are price brackets.
*b) Regression — the output is a continuous number.
c)  Clustering — you're grouping similar cars together.
d)  Reinforcement learning — the model gets rewarded for accurate prices.
... Price is a continuous value (you could output $11,247.83, not just "high/medium/low"), so this is regression. Classification predicts a category from a fixed set. The clue is always "what does the output look like?" — if it's a number on a number line, regression; if it's one of N labels, classification.


3.  After training a model, you want to know how well it will work on new data it has never seen. What's the most reliable way to estimate that?
a)  Check accuracy on the training data — if it's high, the model is good.
*b) Hold out a portion of your data before training, never let the model see it, and evaluate on that held-out set.
c)  Make predictions on the same data you trained on, but only use the first half.
d)  Train the model twice and compare the two scores.
... A model that has seen data during training has effectively memorized it — accuracy on training data is wildly optimistic. The held-out test set is your reality check: it estimates how the model will behave on data it has never seen, which is the only thing that matters in production. Never train on your test set, and don't even peek at it more than you need to, or you'll start (consciously or not) tuning to its quirks.


4.  Keras models accept training data as NumPy arrays. What does NumPy give you that makes it the standard choice here?
a)  A drop-in replacement for pandas DataFrames.
*b) Fast numerical operations on multi-dimensional arrays — vectorized math without Python loops.
c)  Automatic GPU acceleration for all numerical code.
d)  Built-in machine learning algorithms.
... NumPy's superpower is the ndarray — a homogeneous, fixed-size array that supports vectorized operations. Math that would be a slow Python loop runs in optimized C/Fortran underneath. Every modern ML library (Keras, PyTorch, scikit-learn, pandas) is built on top of or interoperates with NumPy. GPU acceleration comes from TensorFlow/PyTorch tensors, not NumPy itself.


5.  You have a CSV with 50,000 rows of patient records (age, weight, lab results, diagnosis). Which Python tool is purpose-built for working with this kind of tabular data before you feed it to a model?
a)  NumPy arrays — for the speed.
*b) A pandas DataFrame.
c)  A Python dictionary keyed by patient ID.
d)  Raw CSV text manipulated with string methods.
... pandas DataFrames are the standard for tabular data — rows, named columns, mixed types, easy filtering, missing-value handling, fast CSV loading. NumPy arrays are great for the numeric tensor you'll eventually pass to Keras, but DataFrames are where you prepare that tensor — clean the data, drop rows, encode categories, then convert to NumPy at the very end with `.to_numpy()` or `.values`.


6.  According to Chollet's framing in Manning Ch 1, what most clearly distinguishes deep learning from earlier machine learning approaches?
a)  Deep learning is always more accurate than traditional ML.
b)  Deep learning only works on images and text.
*c) Deep learning learns its own representations of the data through stacked layers, instead of relying on hand-designed features.
d)  Deep learning runs on GPUs while traditional ML runs on CPUs.
... The headline of Ch 1 is representation learning. Traditional ML usually requires a human to design features — "from a raw image, compute these edge histograms, then feed them to a model." Deep learning learns useful representations directly from raw data by stacking layers, each one building a slightly more abstract representation of the input than the layer below it. That shift is what unlocked vision and language. Accuracy and hardware are downstream consequences, not the defining property.


7.  The first model you build in Keras uses MNIST. What is MNIST, and why is it the "hello world" of deep learning?
a)  A library that ships with TensorFlow.
*b) A small dataset of handwritten digit images, simple enough that a tiny network reaches >97% accuracy with minimal setup — making it ideal for sanity-checking that your training loop works.
c)  A benchmark for large language models.
d)  A new optimizer that replaces SGD.
... MNIST is 70,000 28x28 grayscale images of handwritten digits 0–9. It's small enough to fit in memory, simple enough that even a 2-layer dense network does well, and famous enough that you can compare your numbers against published baselines. Nobody runs MNIST to ship a product — they run it to confirm their environment, code, and intuitions all work before tackling a real problem.


8.  After you build a Keras Sequential model, you call `model.compile(...)`. What does `compile` configure?
a)  It converts your Python code to C++ for faster execution.
b)  It saves the model architecture to disk so you can load it later.
*c) The loss function (what to optimize), the optimizer (how to update weights), and the metrics (what to track during training).
d)  It allocates GPU memory for the model's weights.
... `compile()` is where you tell Keras the training recipe: what to measure (loss), how to improve (optimizer like SGD or Adam), and what to report alongside the loss (metrics like accuracy). It doesn't compile in the C-compiler sense — the name is historical. You can rebuild and recompile a model with different settings to experiment; it's a cheap operation.


9.  In CSC-114, students are split into two tracks: Code Builders and Prompt Masters. What's the difference between them?
a)  Code Builders write code; Prompt Masters only use natural-language prompts and never run code.
*b) Both tracks build the same artifacts, but Code Builders use full Sacred Flow (Issue → Branch → Commit → PR → Merge), while Prompt Masters submit by adding files to the repo via GitHub Desktop or the web upload button.
c)  Code Builders use Python; Prompt Masters use no-code tools.
d)  Code Builders are graded harder than Prompt Masters.
... The two tracks earn identical points on the artifact — the notebook, the write-up, whatever the deliverable is. The difference is in how they submit. Code Builders practice the professional workflow (issue, branch, PR, retro) and earn process credit on top. Prompt Masters keep the friction low and focus on the AI craft. Both are valid success paths in this course.


10. A Code Builder is starting work on this week's spike. In which order should they do these Sacred Flow steps?
a)  Branch → Commit → Open Issue → Merge → Open PR
b)  Commit → Open Issue → Branch → Open PR → Merge
*c) Open Issue → Branch → Commit → Open PR → Merge
d)  Open PR → Branch → Open Issue → Commit → Merge
... Sacred Flow has a deliberate order. The issue comes first — it states what you're about to do and why, before any code exists. The branch gives you a safe place to work. Commits land incrementally as you work. The PR opens once the work is presentable. Merge happens after review. Doing these out of order — especially opening the issue after the work is already done — defeats the point. Sacred Flow is a thinking tool, not a paperwork tool.


11. For Code Builders, the PR description ends with a 1-paragraph retrospective ("what worked / what surprised me / what I'd do differently"). What's the purpose of this retro?
a)  It tells the instructor whether to pass or fail the assignment.
*b) It forces a brief reflection on the process while the experience is still fresh — which is where most of the learning actually sticks.
c)  It's a length requirement that proves you read the assignment.
d)  It replaces the technical write-up.
... The artifact (notebook, write-up) is what you built. The retro is how it went. A real retro answers questions you wouldn't otherwise stop to ask: which part took longer than expected? what surprised you? what would you do differently next time? Three sentences of honest reflection while it's fresh is worth more than ten sentences written a month later. This is also a real-world skill — every functioning engineering team retros somehow.


12. For Code Builders, the Week 2 instructions say to open the GitHub issue *before* you start your spike, not after it's done. Why?
a)  Canvas requires the issue to be created on a specific date.
b)  The issue counts toward the points only if it has the earliest timestamp.
*c) The issue is supposed to state what you intend to try and why — writing it after the work already happened turns it into a status report, not a plan, and skips the thinking step the workflow is designed to create.
d)  Opening the issue after you're done saves time because you already know what you built.
... The issue is your statement of intent. "I'm going to swap the optimizer from SGD to Adam because I want to see if it converges faster" is a hypothesis you can test. Writing that same sentence after the work is already finished is just narration — you've skipped the part where you decided what to learn. This question is most relevant to Code Builders; Prompt Masters skip Sacred Flow entirely.


13. This Knowledge Check (and others like it) allows unlimited attempts. What's the main reason for that?
a)  To make grades higher than they otherwise would be.
b)  Because the quiz is easy and one attempt is enough.
*c) To make the quiz a learning tool — you can try, read the explanation when you miss something, look it up, and try again — rather than a one-shot assessment.
d)  Because the instructor doesn't have time to grade re-takes.
... Knowledge checks here are calibration, not gating. If you miss a question, the explanation tells you exactly what was being asked and why your answer was off — go back to the reading, fix the gap, and retake. That loop (try, fail, learn, retry) is what builds understanding. Save the test anxiety for assessments that actually need it; here, your goal is mastery, not test-taking.
