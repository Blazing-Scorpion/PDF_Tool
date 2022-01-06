import os
from time import sleep
from os import system
import pikepdf
import platform
from tqdm import tqdm
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileMerger
from termcolor import colored


def banner():
    print("""
    
    #######################################################################################
    #######################################################################################
    ###                                                                                 ###
    ###      @@@@@@@   @@@@@@@   @@@@@@@@     @@@@@@@   @@@@@@    @@@@@@   @@@          ###     
    ###      @@@@@@@@  @@@@@@@@  @@@@@@@@     @@@@@@@  @@@@@@@@  @@@@@@@@  @@@          ###
    ###      @@!  @@@  @@!  @@@  @@!            @@!    @@!  @@@  @@!  @@@  @@!          ###
    ###      !@!  @!@  !@!  @!@  !@!            !@!    !@!  @!@  !@!  @!@  !@!          ###
    ###      @!@@!@!   @!@  !@!  @!!!:!         @!!    @!@  !@!  @!@  !@!  @!!          ###
    ###      !!@!!!    !@!  !!!  !!!!!:         !!!    !@!  !!!  !@!  !!!  !!!          ###
    ###      !!:       !!:  !!!  !!:            !!:    !!:  !!!  !!:  !!!  !!:          ###
    ###      :!:       :!:  !:!  :!:            :!:    :!:  !:!  :!:  !:!   :!:         ###
    ###       ::        :::: ::   ::             ::    ::::: ::  ::::: ::   :: ::::     ###
    ###       :        :: :  :    :              :      : :  :    : :  :   : :: : :     ###
    ###                                                                                 ###
    #######################################################################################
    #######################################################################################        
        """)


def no_file():
    print(colored("The File Does not Exist in the Entered Path. Check and Try Again!! Exiting the Software\n", 'red'))
    exit(0)


class PDF_Password:

    def __init__(self, path, password):
        self.path = path
        self.password = password

    def file_exist(self):
        if os.path.isfile(self.path):
            return True
        else:
            return False

    def new_name(self):
        filename, filextension = os.path.split(self.path)
        basename = filextension.split('.')
        basename = basename[0] + '_Encrypted.pdf'
        new_file_name = os.path.join(filename, basename)
        return new_file_name

    def add_password(self):
        new_path = self.new_name()
        pdfWriter = PdfFileWriter()
        pdf = PdfFileReader(self.path)
        for page_num in range(pdf.numPages):
            pdfWriter.addPage(pdf.getPage(page_num))
        pdfWriter.encrypt(self.password)
        with open(new_path, 'wb') as f:
            pdfWriter.write(f)
            f.close()

    def remove_password(self):
        filename, filextension = os.path.split(self.path)
        basename = filextension.split('.')
        basename = basename[0] + "_Decrypted.pdf"
        new_pdf_path = os.path.join(filename, basename)
        with open(self.path, 'rb') as input_file:
            reader = PdfFileReader(input_file)
            try:
                reader.decrypt(self.password)
                output_file = open(new_pdf_path, 'wb')
                writer = PdfFileWriter()
                for i in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(i))
                writer.write(output_file)
            except:
                print(colored(f"\nWrong Password Used. Try Again With Different Password.\n", 'red'))
                system(f"rm -f {new_pdf_path}")
                exit(0)


class PDF_Merger:

    def __init__(self):
        self.paths = []
        self.final_path = None

    @staticmethod
    def file_exist(path):
        if os.path.isfile(path):
            return True
        else:
            return False

    def get_platform(self):
        if str(platform.system()) == "Windows":
            self.final_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            self.final_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

    def get_paths(self):
        print(colored("\nThe Paths of PDF Files Should be Entered in the Order you want to Merge Them!\n", 'yellow'))
        while True:
            user_path = input("Enter the Path to the PDF File and Enter Q/q when Done: ")
            if user_path.lower() != 'q':
                if not self.file_exist(user_path):
                    print(colored("\nThe File Does not Exist in the Provided Path. "
                                  "Check and Try Again!!\n", 'red'))
                    continue
                else:
                    self.paths.append(user_path)
            else:
                if len(self.paths) == 0:
                    print(colored("No Operation was Performed", "red"))
                    exit(0)
                break

    def Merge_PDF(self):
        merger = PdfFileMerger()
        self.get_platform()
        for pdf in self.paths:
            merger.append(pdf)
        merger.write(self.final_path + "/Merged.pdf")
        merger.close()


class PDF_Cracker:

    def __init__(self, pfile, wfile):
        self.pdf_file = pfile
        self.wordlist_file = wfile

    def pdf_file_exist(self):
        if os.path.isfile(self.pdf_file):
            return True
        else:
            return False

    def word_file_exist(self):
        if os.path.isfile(self.wordlist_file):
            return True
        else:
            return False

    def crack_password(self):
        passwords = [line.strip() for line in open(self.wordlist_file, encoding='latin-1').readlines()]
        found_password = None
        for paswrd in tqdm(passwords, "Cracking PDF", unit=" Attempts"):
            try:
                with pikepdf.open(self.pdf_file, password=paswrd):
                    found_password = paswrd
                    break
            except:
                continue
        print('\n')
        if found_password is not None:
            print("Password found:", found_password + '\n')
            print("Thank You For Using the Software. See You Later! \n")
        else:
            print(colored("Password not Found in the Given Wordlist, Try again With Another Wordlist!\n", 'red'))
            exit(0)


if __name__ == '__main__':
    system("clear")
    banner()
    print(colored("Hello! This Software has been Coded to be Used for Educational Purposes Only\n"
                  "Any Misuse of this Software will not be my responsibility\n", 'yellow'))
    print(colored("This Tool Performs Tasks on Only PDF Files.\n", 'yellow'))
    print(colored("Choose One of the Below Given Tasks: \n", 'blue'))
    print(colored("1) Add a Password To a PDF File\n", 'cyan'))
    print(colored("2) Remove Password From a PDF File\n", 'cyan'))
    print(colored("3) Merge Multiple PDF Files\n", 'cyan'))
    print(colored("4) Perform a Dictionary Attack on a PDF File\n", 'cyan'))
    print(colored("5) Exit The Tool\n", 'cyan'))
    user_input = int(input("Enter Your Choice: "))
    print()

    if user_input == 1:
        file_path = input("Enter Path to the PDF File: ")
        print()
        password = input("Enter The Password you want to add to this PDF File: ")
        print()
        pass_adder = PDF_Password(path=file_path, password=password)
        if pass_adder.file_exist():
            pass_adder.add_password()
            print(colored("Your Password has been Added to the PDF FIle and Save in the Same Directory.\n", "green"))
        else:
            no_file()

    elif user_input == 2:
        file_path = input("Enter Path to the PDF File: ")
        print()
        password = input("Enter The Password of the PDF File: ")
        print()
        pass_remover = PDF_Password(path=file_path, password=password)
        if pass_remover.file_exist():
            pass_remover.remove_password()
            print(colored("The Password has been Successfully Removed and the Unprotected PDF has been "
                          "Saved in the Same Directory!!\n", 'green'))
        else:
            no_file()

    elif user_input == 3:
        pdf_merger = PDF_Merger()
        pdf_merger.get_paths()
        pdf_merger.Merge_PDF()
        print(colored("All the PDF Files have been Merged and the Final File has been saved to the Desktop!\n",
                      'green'))
    elif user_input == 4:
        file_path = input("Enter Path to the PDF File: ")
        print()
        word_list = input("Enter The Path to the Wordlist: ")
        print()
        pdf_cracker = PDF_Cracker(pfile=file_path, wfile=word_list)
        if not pdf_cracker.pdf_file_exist():
            print(colored("The PDF File Does Not Exist!\n", 'red'))
            exit(0)
        if not pdf_cracker.word_file_exist():
            print(colored("The Path to the Specified Wordlist does not Exist!\n", 'red'))
            exit(0)
        pdf_cracker.crack_password()
    elif user_input == 5:
        print(colored("\n[!] Exiting the Tool!\n", 'red'))
        sleep(1)
        exit(0)
    else:
        print(colored("[!] Wrong Input! Exiting!!\n", 'red'))
        sleep(1)
        exit(0)
    print(colored("Thank You for Using the Software!!\n", "green"))
