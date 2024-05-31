from ..regression_pipeline import split_into_train_val
from ..regression_pipeline import get_L2_acc
import numpy as np

def test_split_into_train_val():
    train_i = np.arange(6)+4
    frame_train = np.vstack((train_i, train_i, train_i)).T

    expected_train = [(1,frame_train), (2,frame_train)]

    val_i = np.arange(4)
    frame_val = np.vstack((val_i,val_i,val_i)).T
    expected_val = [(1,frame_val),(2,frame_val)]

    R = np.arange(10)
    frame_points = np.vstack((R,R,R)).T
    mean_points = [
        (1,frame_points),
        (2,frame_points)
    ]
    result_train, result_val=split_into_train_val(
        mean_points,x_split=4
    )

    for i,(t, frame) in enumerate(result_train):
        np.testing.assert_equal(t,expected_train[i][0])
        np.testing.assert_array_almost_equal(frame,expected_train[i][1])
    
    for i,(t, frame) in enumerate(result_val):
        np.testing.assert_equal(t,expected_val[i][0])
        np.testing.assert_array_almost_equal(frame,expected_val[i][1])
    
def test_get_L2_acc():
    x = np.linspace(0,1,11)
    def f(x):
        return x**2 + 2*x+3
    y = f(x)
    coord_points = np.vstack((x,y)).T

    coef = np.array([1,2,3])

    expected = 1
    result = get_L2_acc(coef, coord_points)

    np.testing.assert_almost_equal(expected,result)
    
    