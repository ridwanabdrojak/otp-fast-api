import math, random

def generate(length):
  digits = "0123456789"
  otp = ""
  for _ in range(length):
      otp += digits[math.floor(random.random() * 10)]
  return otp
