# pick a target class:
target_label = 954 # banana
# target_label = 99 # goose
# target_label = 543 # dumbell
# target_label = 546 # electric guitar
# target_label = 282 # tiger cat
#target_label = 281 # tabby cat

# start with a random image
act_hist = []

# learning rates -- play with these for different looking results
rate_smooth = .2
rate_obj = 1000
IT = 4000
for it in range(IT):
    if it > 0 and it%100 == 0: print 'iteration {}'.format(it)
    # do a forward pass for the current version of the image
    # and collect the target activation to visualize later
    net.blobs['data'].data[...] = current
    act_hist.append(net.forward(end='fc8')['fc8'].flat[target_label])
    # set the topmost diff and do a backward pass back to the image
    # can also try: `np.arange(1000)==target_label`
    net.blobs['fc8'].diff[...].flat = 2*(np.arange(1000)==target_label)-1
    diff = net.backward(start='fc8')['data']
    # compute smoothness regularization
    x_diff = np.zeros_like(current)
    y_diff = np.zeros_like(current)
    if np.random.rand() > 0.5:
        y_diff[:,1:,:] = (current[:,1:,:] - current[:,:-1,:])
        x_diff[:,:,1:] = (current[:,:,1:] - current[:,:,:-1])
    else:
        y_diff[:,:-1,:] = (-current[:,1:,:] + current[:,:-1,:])
        x_diff[:,:,:-1] = (-current[:,:,1:] + current[:,:,:-1])
    # gradient descent step
    current = current + rate_obj*diff[0] - rate_smooth*x_diff - rate_smooth*y_diff