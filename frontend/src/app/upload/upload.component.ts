import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PdfService } from '../pdf.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss'],
  providers: [PdfService]
})
export class UploadComponent {
  selectedFile: File | null = null;
  uploadSuccess: string | null = null;

  constructor(private pdfService: PdfService, private router: Router) { }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    if (this.selectedFile) {
      const fileNameElement = document.getElementById('fileName');
      if (fileNameElement) {
        fileNameElement.textContent = this.selectedFile.name;
      }
    }
  }

  uploadFile() {
    if (this.selectedFile) {
      this.pdfService.uploadPdf(this.selectedFile).subscribe(
        response => {
          this.uploadSuccess = 'File uploaded successfully!';
          localStorage.setItem('pdfFilePath', response.file_path);
          this.router.navigate(['/chat']);
        },
        error => {
          console.error('Error uploading file', error);
        }
      );
    }
  }
}
