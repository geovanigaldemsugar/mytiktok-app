from mytiktok.helper import Helper



if __name__ == '__main__':
    if not Helper.is_chrome_installed().get('installed'): 
        Helper.install_chrome()
        print(Helper.is_chrome_installed().get('installed'))

        