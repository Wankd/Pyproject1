from tkinter import *
from tkinter import messagebox
import re #正则表达式
import requests
# Button：一个简单的按钮，用来执行一个命令或别的操作。
# Canvas：组织图形。这个部件可以用来绘制图表和图，创建图形编辑器，实现定制窗口部件。
# Checkbutton：代表一个变量，它有两个不同的值。点击这个按钮将会在这两个值间切换。
# Entry：文本输入域。
# Frame：一个容器窗口部件。帧可以有边框和背景，当创建一个应用程序或dialog(对话）版面时，帧被用来组织其它的窗口部件。
# Label：显示一个文本或图象。
# Listbox：显示供选方案的一个列表。listbox能够被配置来得到radiobutton或checklist的行为。
# Menu：菜单条。用来实现下拉和弹出式菜单。
# Menubutton：菜单按钮。用来实现下拉式菜单。
# Message：显示一文本。类似label窗口部件，但是能够自动地调整文本到给定的宽度或比率。
# Radiobutton：代表一个变量，它可以有多个值中的一个。点击它将为这个变量设置值，并且清除与这同一变量相关的其它radiobutton。
# Scale：允许你通过滑块来设置一数字值。
# Scrollbar：为配合使用canvas, entry, listbox, and text窗口部件的标准滚动条。
# Text：格式化文本显示。允许你用不同的样式和属性来显示和编辑文本。同时支持内嵌图象和窗口。
# Toplevel：一个容器窗口部件，作为一个单独的、最上面的窗口显示。
# messageBox：消息框，用于显示你应用程序的消息框。(Python2中为tkMessagebox)
def save_message():
    dbname=dbname_2.get()
    time_=time_2.get()
    if dbname and time_:
        show.delete(1.0,END)
        show.insert('end','保存成功')
    elif dbname:
        show.delete(1.0, END)
        show.insert('end', '设定时间缺失')
    elif time_:
        show.delete(1.0, END)
        show.insert('end', '数据源缺失')
    else:
        show.delete(1.0, END)
        show.insert('end', '请仔细填写')


x=500
y=500
root=Tk()
root.geometry('%sx%s' %(x,y))
root.title('测试')


dbname_0=Label(root,text='数据库名称:',fg='red',font=('宋体',10))
dbname_0.place(x=0,y=0)
dbname_2=Entry(root,font=("宋体",10),fg='green')
dbname_2.place(x=100,y=0)


time_0=Label(root,text='执行时间:',fg='red',font=('宋体',10))
time_0.place(x=0,y=25)
time_2=Entry(root,font=("宋体",10),fg='green')
time_2.place(x=100,y=25)


button_save=Button(root,text='保存',command=save_message)
button_save.place(x=490,y=10,anchor='center')


show=Text(root, width=50,height=10)
show.place(x=0,y=50)


root.mainloop()