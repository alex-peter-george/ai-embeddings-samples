import wx
import logging
import os
import json
from embeddings import correlate_docs

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(1400, 700))

        # Create two panels
        panelA = wx.Panel(self)
        sizerA = wx.BoxSizer(wx.VERTICAL)
        panelA.SetSizer(sizerA)

        panelB = wx.Panel(self)
        sizerB = wx.BoxSizer(wx.VERTICAL)
        panelB.SetSizer(sizerB)
        
        # Create full set of controls to populate the main form
        label0 = wx.StaticText(panelA, label="Web Scrape URL:")
        self.siteurl = wx.TextCtrl(panelA, style=wx.TE_MULTILINE, size= wx.Size(700,50))
        self.siteurl.SetValue("https://www.indeed.com/jobs?q=python&l=New+York%2C+NY&vjk=8bf2e735050604df")
        label1 = wx.StaticText(panelA, label="Web scrape document file:")
        scrapeDocList = ['indeed_sitemap.csv']
        scrapeFiles = wx.ComboBox(panelA, -1, "*select file in the list*", (90, 50), (160, -1), scrapeDocList, wx.CB_DROPDOWN)
        label4 = wx.StaticText(panelA, label="Bot response:")
        self.botresponse = wx.TextCtrl(panelA, style=wx.TE_MULTILINE, size= wx.Size(700,500))
        
        label2 = wx.StaticText(panelB, label="Source document file:")
        sourceDocList = ['AlexGeorgescu.pdf']
        sourceFiles = wx.ComboBox(panelB, -1, "*select file in the list*", (90, 50), (160, -1), sourceDocList, wx.CB_DROPDOWN)
        label3 = wx.StaticText(panelB, label="Source document content:")
        self.sourceContent = wx.TextCtrl(panelB, style=wx.TE_MULTILINE, size= wx.Size(700,700))
                
        # Customize the appearance of "ask the bot" button to stand out
        btnaskbot = wx.Button(panelA, label="Ask the Bot")
        btnaskbot.SetBackgroundColour(wx.Colour(255, 230, 200))  # Set the background color
        # Create a bold font
        font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        btnaskbot.SetFont(font)

        sizerA.Add(label0, flag=wx.ALL, border=5)
        sizerA.Add(self.siteurl, flag=wx.ALL, border=5)
        sizerA.Add(label1, flag=wx.ALL, border=5)
        sizerA.Add(scrapeFiles, flag=wx.ALL, border=5)
      
        sizerA.Add(btnaskbot, flag=wx.ALL, border=5)

        sizerA.Add(label4, flag=wx.ALL, border=5)
        sizerA.Add(self.botresponse, flag=wx.ALL, border=5)

        sizerB.Add(label2, flag=wx.ALL, border=5)
        sizerB.Add(sourceFiles, flag=wx.ALL, border=5)
        sizerB.Add(label3, flag=wx.ALL, border=5)
        sizerB.Add(self.sourceContent, flag=wx.ALL, border=5)
        

        # Arrange the panels side by side using a horizontal sizer
        winsizer = wx.BoxSizer(wx.HORIZONTAL)
       
        winsizer.Add(panelA, 1, wx.EXPAND)
        winsizer.Add(panelB, 2, wx.EXPAND)
        self.SetSizer(winsizer)

        # Bind the buttons click event to handlers
        btnaskbot.Bind(wx.EVT_BUTTON, self.OnAskBotButton)

        # Bind the combos selections to handlers
        scrapeFiles.Bind(wx.EVT_COMBOBOX, self.OnSelectedScrapeFile)
        sourceFiles.Bind(wx.EVT_COMBOBOX, self.OnSelectedSourceFile)
    
    def OnSelectedScrapeFile(self, e):
        # Populate the bot role to generate summary
        i = 3

    def OnSelectedSourceFile(self, e):
        # Populate the bot role to generate summary
        filename = e.String
        self.sourceContent.SetValue(correlate_docs.ExtractTextFromPdf(filename))
    
    def OnAskBotButton(self, e):
        # Generate scraped web document

        response = correlate_docs.RunWebScrape(self.siteurl.GetValue())
        if response['error']:
           self.botresponse.SetValue(f"[ERROR]:{response['error']}") 
        else:
            self.botresponse.SetValue(f"{response['response']}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, title="Engage Bot with Open AI")
    frame.Show()
    app.MainLoop()


