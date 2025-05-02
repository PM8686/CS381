# CS381
Introduction to Machine Learning


Choosing which models to use:
- Perceptron: best for binary classification, which is not what we are doing here
- logistic regression: good for what we want to do, with momentum stochastic gradient descent, given the N >>> d, that method will limit the impact of N on the time it takes.
- Kernel ridge regression: good for nonlinear relationships, however the time it taks is dependent on N not d, and our N is > 100,000 so may not be the best choice. 
- Principal Component Analysis: our dimensions are still relatively small, so may not be needed, but would be interesting visually, also our dataset is more so about regression than it is classification.