from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType 
import sys
from navarp.utils import navfile
import numpy as np
import h5py

from gui import Ui_Form  as ui  




class MainWindow(QWidget, ui):

    def __init__(self):
        QWidget.__init__(self)
        #self.setWindowIcon(QtGui.QIcon('logo.jpg')) choose logo from the designer
        self.setupUi(self)
        self.HandleButtons()

       
        
        
    def HandleButtons(self):
        self.browse_pushButton.clicked.connect(lambda: self.openFileNameDialog())
        self.export_pushButton.clicked.connect(lambda: self.open_save_dialog_exp())
        self.delete_pushButton.clicked.connect(lambda: self.open_save_dialog_info())



    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","ZIP (*.zip)", options=options)
        if self.fileName:
            print(self.fileName)
            self.set_file_path(self.fileName) 
            
                  

    def open_save_dialog_exp(self):
        option = QFileDialog.Options()
        option |=  QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(self, "Save File Name Title", f"{self.fileName[:-4]}_info.txt", "All Files (*)", options=option)
        if self.fileName:
            notes = self.extract_info(self.fileName)
            with open(file[0], 'w', encoding='utf-8') as f:
                f.write(notes)
                
        QMessageBox.information(self, 'Information',
                                        f"Info txt file exported as {self.fileName[:-4]}.txt" ,
                                        QMessageBox.Ok)
            
    def open_save_dialog_info(self):
        option = QFileDialog.Options()
        option |=  QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(self, "Save File Name Title", f"{self.fileName[:-4]}.h5", "All Files (*)", options=option)
        if self.fileName:
            base_file_name = file[0]
            self.convert2h5(self.fileName,base_file_name)

        QMessageBox.information(self, 'Information',
                                        f"HDF5 file exported as {self.fileName[:-4]}.h5" ,
                                        QMessageBox.Ok)
            

        
       
    def extract_info(self,path):
        if path[-4:] == '.zip':
            file_ext = 'ZIP file'
            entry = navfile.load(path) 
        else:
            raise ValueError("Input data must be zip file!")
        
        notes_text=''
        notes_text+='It is '+file_ext+' file ! '+ "\n"
        notes_text+='Excitation energy beam h\u03BD = '+ str(np.round(entry.hv[0],2)) +' eV'
        notes_text+='Pass energy = ' + str(entry.file_note[88:92])+' eV'+ "\n"
        notes_text+='\n'
        notes_text+='File contain '+str(len(entry.scans))+' scans corresponding to : '+ '\u03C6 (nommé \u03B8 en Cassiopee) = '+str(np.round(entry.scans[0],2))+'° : '+str(np.round(entry.scans[-1],2))+str('°')
        notes_text+='File contain '+str(len(entry.angles))+' angles value (analyzer slit) corresponding to : '+ '\u03B8 = '+str(np.round(entry.angles[0],2))+'° : '+str(np.round(entry.angles[-1],2))+str('°')+ "\n"
        notes_text+='File contain '+str(len(entry.energies))+' energies value corresponding to : E = '+str(np.round(entry.energies[0],2))+' eV : '+str(np.round(entry.energies[-1],2))+str(' eV')+ "\n"
        notes_text+='\n'+'==================  '+ 'Matrix shape = '+ str(np.shape(entry.data))+'  =================='

        return notes_text
    




        
    

        

   
 

    def convert2h5(self,path,output_file):
        # Load the zip file
        if path[-4:] == '.zip':
            entry = navfile.load(path) 
        else:
            raise ValueError("Input data must be zip file!")
        # Export to HDF5 format
        with h5py.File(output_file, 'w') as f:
            f.create_dataset('matrix', data=entry.data)
        

    


        
    



  
            

        


    def set_file_path(self,file_path):
        self.path_lineEdit.setText(file_path)

    

    # def extract_notes(self,path):
    #     ppt=Presentation(path)
    #     notes = []
    #     for page, slide in enumerate(ppt.slides):
    #         # this is the notes that doesn't appear on the ppt slide,
    #         # but really the 'presenter' note. 
    #         textNote = slide.notes_slide.notes_text_frame.text
    #         notes.append((page,textNote)) 
    #     return notes
    
   
    
      




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # hold ui
    app.exec_()

if __name__ == "__main__" :
    main()



