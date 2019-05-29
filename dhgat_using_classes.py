# import libraries
from selenium import webdriver
from urllib.request import urlretrieve
import pandas as pd
from tkinter import *
import os

class Get_product:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='C:/Users/shree/web_scrapping_project/chromedriver')
    def get_product_name(self,name):
        self.product = name
        return self.product

class Getlinks(Get_product):
    def __init__(self):
        Get_product.__init__(self)
        self.a=Get_product.get_product_name(self,name=get_produc_details())

    def get_links(self):
        self.driver.get("https://www.dhgate.com/wholesale/search.do?act=search&sus=&searchkey={}".format(
            '+'.join((self.a).split())))
        self.links = self.driver.find_elements_by_xpath('.//h3[@class="pro-title"]/a')
        self.all_links = []
        for i in self.links:
            self.all_links.append(str(i.get_attribute('href')))
        return self.all_links

class Getdata(Getlinks):
    data=[]
    def __init__(self):
        Getlinks.__init__(self)

    def get_data(self):
        for i in Getlinks.get_links(self):
            self.driver.get(i)
            self.d = {}

            self.d['name'] = (self.driver.find_element_by_xpath('//div[@class="hinfo clearfix"]/h1')).text
            try:
                self.d['ratings'] = (self.driver.find_element_by_xpath('//li[@class="li1"]')).text
            except:
                self.d['ratings'] = "not found"
            self.d['price'] = \
            ((self.driver.find_element_by_xpath('//div[@class="key-info-ri clearfix pricearea pricearea-lot"]')).text).split(
                "/")[0]
            try:
                self.d['reviews'] = (self.driver.find_element_by_xpath('//a[@id="anchor-productReviews"]/span')).text
            except:
                self.d['reviews']="Not found"


            self.img = self.driver.find_element_by_xpath('//div[@class="bimg-inner"]/span/img')
            self.src = self.img.get_attribute('src')
            urlretrieve(self.src, "{}".format((str(self.src).split('/')[-1])))
            self.d['image'] = (str(self.src).split('/')[-1])
            Getdata.data.append(self.d)

        return Getdata.data
class DataToCsv(Getdata):
    def __init__(self):
        Getdata.__init__(self)

    def data_to_csv(self):
        self.df = pd.DataFrame(Getdata.get_data(self))
        self.df.to_csv("dhgate.csv", index=False)
        self.driver.close()
def get_produc_details():
    x=str(entry1.get())
    return x
def read_rext():
    #obj=Get_product()
    #obj.get_product_name(get_produc_details())
    obj1 = DataToCsv()
    obj1.get_product_name(get_produc_details())
    obj1.data_to_csv()


def find_product1():


    try:
        variable.set("select product")
        data = pd.read_csv("dhgate.csv")
        df1 = data['image']
        l = [i for i in df1]
        heading2 = Label(root, text="Select product :", font=('arial', 18, 'bold'), fg='steelblue').place(x=60, y=190)
        w = OptionMenu(root, variable, *l).place(x=260, y=192)
        submit3 = Button(root, text="Submit", width=10, height=1, bg="white", command=get_product_details).place(x=400,
                                                                                                                 y=196)
    except:
        variable.set("select product")
        heading2 = Label(root, text="Select product :", font=('arial', 18, 'bold'), fg='steelblue').place(x=60, y=190)
        w = OptionMenu(root, variable, "not found").place(x=260, y=192)
        submit3 = Button(root, text="Submit", width=10, height=1, bg="white", command="").place(x=400, y=196)


def get_product_details():
    b=variable.get()
    root1 = Tk()
    root1.geometry("1400x500+0+0")
    try:
        data = pd.read_csv("dhgate.csv")
        data.set_index("image", inplace=True)
        a = (data.loc['{}'.format(b)])


        T = Text(root1, height=10, width=100)
        T.pack()
        T.insert(END, "\nName    :{} doller".format(a[0]))
        T.insert(END, "\nPrice   :{}".format(a[1]))
        T.insert(END, "\nRatings :{}".format(a[2]))
        T.insert(END, "\nReviwes :{}".format(a[3]))

    except:
        T = Text(root1, height=10, width=100)
        T.pack()
        T.insert(END, "{data not found}")

    root1.mainloop()


root = Tk()
root.title('NEW APPLICATION')
root.geometry("500x250+0+0")
heading1=Label(root,text="Enter product :",font=('arial',18,'bold'), fg='steelblue').place(x=60,y=80)
entry1=StringVar()
entry_box1=Entry(root, textvariable=entry1, width=25, bg='white').place(x=250,y=90)
submit1=Button(root,text="Submit" ,width=10,height=1,bg="white" ,command=read_rext).place(x=170,y=120)
submit2=Button(root,text="Cancel" ,width=10,height=1,bg="white",command=root.destroy).place(x=280,y=120)
refresh=Button(root,text="Refresh" ,width=10,height=1,bg="white",command=find_product1).place(x=420,y=0)
find=Button(root,text="search" ,width=8,height=1,bg="white",command=find_product1).place(x=0,y=190)
variable = StringVar(root)
root.mainloop()
#obj1=DataToCsv()
#obj1.data_to_csv()
