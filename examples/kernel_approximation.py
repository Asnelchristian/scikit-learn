"""
================================
Recognizing hand-written digits
================================

An example showing how the scikit-learn can be used to recognize images of
hand-written digits.

This example is commented in the
:ref:`tutorial section of the user manual <getting_started>`.

"""
print __doc__

# Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
#         modified Andreas Mueller
# License: Simplified BSD

# Standard scientific Python imports
import pylab as pl

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics, pipeline
from sklearn.feature_extraction.kernel_approximation import RBFSampler

# The digits dataset
digits = datasets.load_digits()

# The data that we are interested in is made of 8x8 images of digits,
# let's have a look at the first 3 images, stored in the `images`
# attribute of the dataset. If we were working from image files, we
# could load them using pylab.imread. For these images know which
# digit they represent: it is given in the 'target' of the dataset.
for index, (image, label) in enumerate(zip(digits.images, digits.target)[:4]):
    pl.subplot(2, 4, index+1)
    pl.imshow(image, cmap=pl.cm.gray_r)
    pl.title('Training: %i' % label)

# To apply an classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
kernel_svm = svm.SVC(gamma=0.001)
linear_svm = svm.LinearSVC()

# create pipeline from kernel approximation
# and linear svm
feature_map = RBFSampler(gamma=0.001, D=5000)
approx_kernel_svm = pipeline.Pipeline([("feature_map", feature_map),
    ("svm", svm.LinearSVC())])

for classifier in [kernel_svm, linear_svm, approx_kernel_svm]:
    # We learn the digits on the first half of the digits
    classifier.fit(data[:n_samples/2], digits.target[:n_samples/2])

    # Now predict the value of the digit on the second half:
    expected = digits.target[n_samples/2:]
    predicted = classifier.predict(data[n_samples/2:])

    print "Classification report for classifier %s:\n%s\n" % (
        classifier, metrics.classification_report(expected, predicted))
    print "Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted)
