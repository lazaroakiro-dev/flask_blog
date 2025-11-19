def product_except_self(nums):
    n = len(nums)
    output = [1] * n
    print (output)
    
    # Step 1: prefix products
    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]
        
        print(output)
    
    # Step 2: suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]
        
    
    return output

# Example usage
nums = [1, 2, 3, 4]
print(product_except_self(nums))  # [24, 12, 8, 6]