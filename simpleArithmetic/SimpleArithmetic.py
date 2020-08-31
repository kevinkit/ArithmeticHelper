# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 08:24:33 2020

@author: KHoefle
"""
import numpy as np
class MulConstant:
    def __init__(self, 
                 constant,
                 name,
                 allowed_error = 1024,
                 maximum_allowed_bit_shift=16):
        
        self.constant = constant
        self.constant_object = np.array(constant,dtype=np.object)
        self.allowed_error = 1024
        self.maximum_allowed_bit_shift = maximum_allowed_bit_shift
        self.name = name
        
    def __call__(self, x):
        
        original_dtype = x.dtype
        # here we test the result
        desired_result = np.array(x,dtype=np.object) * self.constant_object 
        result = x * self.constant
        
        if not (desired_result == result).any():
            
            err = self.allowed_error*2#np.mean(np.abs(desired_result - result))
            
            shift_cnt = 1
            while err > self.allowed_error:
                
                result = np.array(x/(2**shift_cnt),dtype=x.dtype)  * self.constant
                desired_result = np.array(x/(2**shift_cnt),dtype=np.object) * self.constant_object 
                err = np.mean(np.abs(desired_result - result))
                
                if shift_cnt == self.maximum_allowed_bit_shift:
                    raise ArithmeticError("Maximum allowed shift bits exceeded:",
                                          shift_cnt,
                                          "and error is at:",
                                          err,
                                          "at",
                                          self.name)
                    
                shift_cnt += 1
            print("shift at\n",self.name,"for",shift_cnt)
        
        if result.dtype != original_dtype:
            raise ArithmeticError("Cannot do the operation",
                                  self.name,
                                  "without chaning the bit width from",
                                  original_dtype,"to",
                                  result.dtype)
               
        return result
 
class AddConstant:
    def __init__(self, 
                 constant,
                 name,
                 allowed_error = 1024,
                 maximum_allowed_bit_shift=16):
        
        self.constant = constant
        self.constant_object = np.array(constant,dtype=np.object)
        self.allowed_error = 1024
        self.maximum_allowed_bit_shift = maximum_allowed_bit_shift
        self.name = name
        
    def __call__(self, x):
        
        original_dtype = x.dtype
        # here we test the result
        desired_result = np.array(x,dtype=np.object) + self.constant_object 
        result = x + self.constant
        
        if not (desired_result == result).any():
            
            err = self.allowed_error*2#np.mean(np.abs(desired_result - result))
            
            shift_cnt = 1
            while err > self.allowed_error:
                
                result = np.array(x/(2**shift_cnt),dtype=x.dtype) + self.constant
                desired_result = np.array(x/(2**shift_cnt),dtype=np.object) + self.constant_object 
                err = np.mean(np.abs(desired_result - result))
                
                if shift_cnt == self.maximum_allowed_bit_shift:
                    raise ArithmeticError("Maximum allowed shift bits exceeded:",
                                          shift_cnt,
                                          "and error is at:",
                                          err,
                                          "at",
                                          self.name)
                    
                shift_cnt += 1
            print("shift at\n",self.name,"for",shift_cnt)
        
        if result.dtype != original_dtype:
            raise ArithmeticError("Cannot do the operation",
                                  self.name,
                                  "without chaning the bit width from",
                                  original_dtype,"to",
                                  result.dtype)
               
        return result
 
    
class MulSignals:
    def __init__(self, 
                 name,
                 allowed_error = 1024,
                 maximum_allowed_bit_shift=16):
        
        self.allowed_error = 1024
        self.maximum_allowed_bit_shift = maximum_allowed_bit_shift
        self.name = name
        
    def __call__(self, x):
        """
            x is a list of signals which are all going to be multiplied with
            each other. The datatype is determined by the first entry in the list
        """
               
        original_dtype = x[0].dtype
        
        shape_vec = x[0].shape

        input_shape_vec = []
        input_shape_vec.append(len(x))
        for entry in shape_vec:
            input_shape_vec.append(entry)
        
        signals_object = np.zeros(shape=input_shape_vec,dtype=np.object)
        for cnt,entry in enumerate(x):
            signals_object[cnt] = np.array(entry,dtype=np.object)
    
        desired_result = np.ones(shape=shape_vec,dtype=np.object) 
        for entry in signals_object:
            desired_result *= entry
        
        result = np.ones(shape=shape_vec,dtype=original_dtype)
        for entry in x:
              result *= entry        
        if not (desired_result == result).any():
            err = self.allowed_error*2#np.mean(np.abs(desired_result - result))
            
            shift_cnt = 1
            while err > self.allowed_error:        

                desired_result = np.ones(shape=shape_vec,dtype=np.object) 
                for entry in signals_object:
                    desired_result *= np.array(entry / 2**shift_cnt,dtype=np.object)
                
                result = np.ones(shape=shape_vec,dtype=original_dtype)
                for entry in x:
                      result *= np.array(entry / 2**shift_cnt,dtype=original_dtype)
                      
                err = np.mean(np.abs(desired_result - result))
                
                if shift_cnt == self.maximum_allowed_bit_shift:
                    raise ArithmeticError("Maximum allowed shift bits exceeded:",
                                          shift_cnt,
                                          "and error is at:",
                                          err,
                                          "at",
                                          self.name)
                    
                shift_cnt += 1
            print("shift at\n",self.name,"for",shift_cnt)
        
        if result.dtype != original_dtype:
            raise ArithmeticError("Cannot do the operation",
                                  self.name,
                                  "without chaning the bit width from",
                                  original_dtype,"to",
                                  result.dtype)        
        return result
    
class AddSignals:
    def __init__(self, 
                 name,
                 allowed_error = 1024,
                 maximum_allowed_bit_shift=16):
        
        self.allowed_error = 1024
        self.maximum_allowed_bit_shift = maximum_allowed_bit_shift
        self.name = name
        
    def __call__(self, x):
        """
            x is a list of signals which are all going to be added with
            each other. The datatype is determined by the first entry in the list
        """
               
        original_dtype = x[0].dtype
                   
        shape_vec = x[0].shape
        
        input_shape_vec = []
        input_shape_vec.append(len(x))   
        for entry in shape_vec:
            input_shape_vec.append(entry)
        
        signals_object = np.zeros(shape=input_shape_vec,dtype=np.object)
        for cnt,entry in enumerate(x):
            signals_object[cnt] = np.array(entry,dtype=np.object)
    
        desired_result = np.ones(shape=shape_vec,dtype=np.object) 
        for entry in signals_object:
            desired_result += entry
        
        result = np.ones(shape=shape_vec,dtype=original_dtype)
        for entry in x:
              result += entry        
        if not (desired_result == result).any():
            err = self.allowed_error*2#np.mean(np.abs(desired_result - result))
            
            shift_cnt = 1
            while err > self.allowed_error:        

                desired_result = np.ones(shape=shape_vec,dtype=np.object) 
                for entry in signals_object:
                    desired_result += np.array(entry / 2**shift_cnt,dtype=np.object)
                
                result = np.ones(shape=shape_vec,dtype=original_dtype)
                for entry in x:
                      result += np.array(entry / 2**shift_cnt,dtype=original_dtype)
                      
                err = np.mean(np.abs(desired_result - result))
                
                if shift_cnt == self.maximum_allowed_bit_shift:
                    raise ArithmeticError("Maximum allowed shift bits exceeded:",
                                          shift_cnt,
                                          "and error is at:",
                                          err,
                                          "at",
                                          self.name)
                    
                shift_cnt += 1
            print("shift at\n",self.name,"for",shift_cnt)
        
        if result.dtype != original_dtype:
            raise ArithmeticError("Cannot do the operation",
                                  self.name,
                                  "without chaning the bit width from",
                                  original_dtype,"to",
                                  result.dtype)        
        return result

# simple test case 
if __name__ == '__main__':
        
    # (2*((x + 16)^2 + (x+16)^3) + 1024) / 1024
        
    # initialize signal    
    #x = np.array([2**10,2**10,2**10],dtype=np.uint32)
    #x = np.random.randint(0,2**20,dtype=np.uint32,size=(100,100,3))
    x = np.ones(shape=(100,100,3),dtype=np.uint32)*(2**16)
    x_first_mul = MulConstant(2**4,name="First Multiplication")(x)
    
    x2 = MulSignals(name="square")([x_first_mul,x_first_mul])
    x3 = MulSignals(name="cubic",maximum_allowed_bit_shift=16)([x_first_mul,x_first_mul,x_first_mul])
    
    x = AddSignals(name="Addition")([x2,x3])
    x = AddConstant(2**10, "Adding 1024")(x)
    
    # subtractions and division can be done like this, cause they should not 
    # use more bit. If a fractional division is done, it should be done with a 
    # multiplication instead like: x/0.5 = x*2
    x = x - 1024
    x = np.array(x / 1024,dtype=x.dtype)
    print(x.dtype)
    
    y = AddSignals(name="Addition")([x,x])      
    
    #print(y)