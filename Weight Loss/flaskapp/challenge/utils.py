
def bmi_calculator(metric, weight, height_ft, height_in):

    if metric == 'Pounds':
        weight = weight / 2.205
    else:
        weight = weight
    
    height_in += height_ft * 12
    height_cm = round(height_in * 2.54, 2)

    # BMI Formula
    bmi = round(weight / ((height_cm/100) ** 2),1)

    # BMI Range
    if(bmi>0):
        if(bmi<=16):
            category = "Very Underweight"
        elif(bmi<18.5):
            category = "Underweight"
        elif(bmi<=24.9):
            category = "Normal"
        elif(bmi<=30):
            category = "Overweight"
        else: 
            category = "Obese."

    return bmi, category

# bmi_calculator('Pounds', 149.0, 5, 5)

def test_posts(posts):

    for post in posts:
        print(post)