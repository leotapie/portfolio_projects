This projects looks at classifying images of dogs and cats (from the [2013 kaggle competition](https://www.kaggle.com/c/dogs-vs-cats/overview)). I've fine tunned the convolution neural network (CNN) model: VGG16 to achieve binary image classification ([VGG16](https://datagen.tech/guides/computer-vision/vgg16/#) was initially designed to classify images across 1000 classes). This was achieve using the `tensorflow` machine learning library and `keras` API.

The dataset used can be found and downloaded [here](https://www.kaggle.com/c/dogs-vs-cats/data).

My work can be found in this [notebook]() (Performance: 95% accuracy on validation set!). Briefly explanation to follow the notebook:

### 1 - Loading and preprocessing the data
- Extract the labels from the training data filenames
- Split training data to have a validation set, create dataframes with images' path and labels

### 2 - Build the model
In order to keep the running time reasonable a few steps were taken:
- 128x128 image input size (rather than the 224x224 of the VGG16 architecture)
- the first 15 layers of the pre-trained VGG16 model were set to untrainable

The added layers at the end pre-trained model are design to flatten the output to 1-dimension through the very last fully connected softmax layer (i.e. between 0 and 1, to achieve the binary classification). Note that a dropout layer was also added to help with avoiding overfitting to the training data. 

The metric of interest chosen is the **validation accuracy**. For more detail about the loss function, optimizer and callbacks chosen please refer to the notebook. 

### 3 - Define the generators
Three image generators were defined based on the dataframe created in the preprocessing steps. The generators are used in the training (`model.fit()`) and testing (`model.predict()`) steps respectively - essentially providing the model with the path to the images, the labels (where applicable) and data extraction. 

### 4 - Train the model 

### 5 - Asess performance on the validation set
<img width="410" alt="image" src="https://github.com/leotapie/portfolio_projects/assets/141837622/36848547-9ad5-48fe-ab5e-10b1fab0f40f">

