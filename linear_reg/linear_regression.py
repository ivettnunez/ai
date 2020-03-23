import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

__errors__= [];


def hyp(params, x):
    y_model = 0
    for i in range(len(params)):
        y_model += params[i] * x[i]

    return y_model

def gradient_descent(params, samples, y_real, alfa):
    n = len(samples)
    new_params = list(params)
    for i in range(len(params)):
        sumatory = 0
        for j in range(n):
            sumatory += ( hyp(params, samples[j]) - y_real[j] ) * samples[j][i]

        new_params[i] = params[i] - ( (alfa/n) * sumatory)

    return new_params


def tracking_error(params, samples, y_real):
    acum = 0

    for i in range(len(samples)):
        y_model = hyp(params,samples[i])
        #print( "y_model  %f  y_real %f " % (y_model,  y_real[i]))
        acum += (y_model-y_real[i])**2

    mean_square_error = acum/len(samples)
    __errors__.append(mean_square_error)


def get_y_model(params, samples):
    y = []
    for i in range(len(samples)):
        y_model = hyp(params,samples[i])
        y.append(y_model)
    return y



def normalize(samples):
    acum = 0
    samples = np.asarray(samples).T.tolist()
    #iterate over samples
    for i in range(1, len(samples)):
        #iterate over sample's features to get average
        for j in range(len(samples[i])):
            acum =+ samples[i][j]

        avg = acum / len(samples[i])
        max_value = max(samples[i])

        #iterate over sample's features to normalize values
        for j in range(len(samples[i])):
            samples[i][j] = (samples[i][j] - avg)/max_value

    return np.asarray(samples).T.tolist()



# Get samples
data = pd.read_csv('estimations.csv')
original_samples = list(data['x'])
samples = list(data['x'])
y_real = list(data['y'])

params = [0,0]
alfa = 0.03
epochs = 0
limit = 150


# Add x0 for each sample
for i in range(len(samples)):
    samples[i] = [1, samples[i]]


# Scaling samples
samples = normalize(samples)

# Gradient descent to minimize the cost function
# until reach the minimum the cost function
while epochs < limit:
    previous_params = list(params)
    params = gradient_descent(params, samples, y_real, alfa)
    #tracking_error(params, samples, y_real)
    print("Parameters: " + str(params))
    if(previous_params == params):
        break

    epochs += 1

print("Final parameters = " + str(params))

# Plot error
#plt.plot(__errors__)
#plt.show()

# Plot the model
y_model = get_y_model(params, samples)
#print("y model " + str(y_model))
#print("y real " + str(y_real))

plt.plot(original_samples, y_real, 'ro')
plt.plot(original_samples, y_model)
plt.show()

# Using parameters value in the hypothesis function
# to predict the y of new x values
data = pd.read_csv('test.csv')
test_samples = list(data['x'])
# Add x0 for each test sample
for i in range(len(test_samples)):
    test_samples[i] = [1, test_samples[i]]

original_test = test_samples[-1]

# Scaling test samples
test_samples = normalize(test_samples)

test_value = list(test_samples[-1])
prediction = hyp(params, test_value)

# Plot prediction
plt.plot(original_samples, y_real, 'ro')
plt.plot(original_test[1], prediction, 'gs')

#original_samples.append(test_value[1])
#y_model. append(prediction)
plt.plot(original_samples, y_model)
#plt.show()
