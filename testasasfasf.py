def asfsafsaf(test1, test2):
    return test1, test2

a = {
    'methods': asfsafsaf,
    'attrs': ['test_1', 'test_2']
}

print(a['methods'](*a['attrs']))