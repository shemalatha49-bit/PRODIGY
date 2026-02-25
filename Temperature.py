"""
Temperature Conversion Program
Converts temperatures between Celsius, Fahrenheit, and Kelvin
"""

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit
    Formula: (C × 9/5) + 32
    """
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    """
    Convert Celsius to Kelvin
    Formula: C + 273.15
    """
    return celsius + 273.15

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius
    Formula: (F − 32) × 5/9
    """
    return (fahrenheit - 32) * 5/9

def kelvin_to_celsius(kelvin):
    """
    Convert Kelvin to Celsius
    Formula: K − 273.15
    """
    return kelvin - 273.15

def convert_temperature(value, unit):
    """
    Convert temperature from one unit to all other units
    
    Args:
        value: Temperature value (float)
        unit: Original unit ('C', 'F', or 'K')
    
    Returns:
        Dictionary with converted values or None if invalid
    """
    unit = unit.upper()
    
    # Validate physical limits
    if unit == 'K' and value < 0:
        print("Error: Kelvin cannot be negative (absolute zero is 0 K)")
        return None
    elif unit == 'C' and value < -273.15:
        print("Error: Temperature cannot be below absolute zero (-273.15°C)")
        return None
    elif unit == 'F' and value < -459.67:
        print("Error: Temperature cannot be below absolute zero (-459.67°F)")
        return None
    
    # Perform conversions based on input unit
    if unit == 'C':
        fahrenheit = celsius_to_fahrenheit(value)
        kelvin = celsius_to_kelvin(value)
        return {
            'original': f"{value}°C",
            'fahrenheit': fahrenheit,
            'kelvin': kelvin
        }
    
    elif unit == 'F':
        celsius = fahrenheit_to_celsius(value)
        kelvin = celsius_to_kelvin(celsius)
        return {
            'original': f"{value}°F",
            'celsius': celsius,
            'kelvin': kelvin
        }
    
    elif unit == 'K':
        celsius = kelvin_to_celsius(value)
        fahrenheit = celsius_to_fahrenheit(celsius)
        return {
            'original': f"{value} K",
            'celsius': celsius,
            'fahrenheit': fahrenheit
        }
    
    else:
        print(f"Error: Invalid unit '{unit}'. Please use C, F, or K.")
        return None

def display_results(results):
    """
    Display conversion results in a formatted way
    """
    print("\n" + "="*40)
    print("CONVERSION RESULTS")
    print("="*40)
    print(f"Original Temperature: {results['original']}")
    print("-"*40)
    
    # Display other two units
    for key, value in results.items():
        if key != 'original':
            if key == 'celsius':
                print(f"Celsius: {value:.2f}°C")
            elif key == 'fahrenheit':
                print(f"Fahrenheit: {value:.2f}°F")
            elif key == 'kelvin':
                print(f"Kelvin: {value:.2f} K")
    print("="*40 + "\n")

def main():
    """
    Main program function
    """
    print("="*40)
    print("TEMPERATURE CONVERSION PROGRAM")
    print("="*40)
    
    # Get temperature value
    while True:
        try:
            temp_value = float(input("\nEnter temperature value: "))
            break
        except ValueError:
            print("Error: Please enter a valid numeric value.")
    
    # Get unit of measurement
    print("\nChoose unit:")
    print("  C - Celsius")
    print("  F - Fahrenheit")
    print("  K - Kelvin")
    
    while True:
        unit = input("\nEnter unit (C/F/K): ").strip().upper()
        if unit in ['C', 'F', 'K']:
            break
        else:
            print("Error: Please enter C, F, or K.")
    
    # Perform conversion
    results = convert_temperature(temp_value, unit)
    
    # Display results if conversion was successful
    if results:
        display_results(results)
        
        # Ask if user wants to convert another temperature
        another = input("Convert another temperature? (y/n): ").strip().lower()
        if another == 'y':
            print("\n")
            main()  # Recursive call to start over
        else:
            print("\nThank you for using the Temperature Conversion Program!")

# Run the program
if __name__ == "__main__":
    main()
