def asceTable(vs100):
    site_class_dict = {
        range(0, 501): 'E',
        range(501, 701): 'DE',
        range(701, 1001): 'D',
        range(1001, 1451): 'CD',
        range(1451, 2101): 'C',
        range(2101, 3001): 'BC',
        range(3001, 5001): 'B',
        range(5001, 10000): 'A'
    }
    for key in site_class_dict:
        if vs100 in key:
            return site_class_dict[key]
        
def main():
    test_values = [250, 750, 1000, 1001, 5500]
    for value in test_values:
        letter = asceTable(value)
        print(f'The value {value} correlates to site class {letter}')

if __name__ == "__main__":
    main()