import c4d

def main():
    for i in dir(c4d):
        if i.startswith('ID_SOUND'):
            val = c4d.__dict__[i]
            print i, val
            
if __name__ == '__main__':
    main()
