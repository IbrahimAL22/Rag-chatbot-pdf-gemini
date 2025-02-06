import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PdfService } from '../pdf.service';

@Component({
  selector: 'app-query',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.scss'],
  providers: [PdfService]
})
export class QueryComponent implements OnInit {
  query: string = '';
  messages: { sender: string, text: string }[] = [];
  pdfName: string = '';

  constructor(private pdfService: PdfService, private router: Router) { }

  ngOnInit() {
    // Retrieve the PDF name from local storage or any other source
    const pdfFilePath = localStorage.getItem('pdfFilePath');
    if (pdfFilePath) {
      this.pdfName = this.extractFileName(pdfFilePath);
    }
  }

  sendQuery() {
    const filePath = localStorage.getItem('pdfFilePath');
    if (filePath && this.query.trim()) {
      // Add user message to the array immediately
      this.messages.push({ sender: 'User', text: this.query.trim() });

      this.pdfService.queryPdf(filePath, this.query.trim()).subscribe(
        response => {
          // Add bot response to the array after receiving it
          this.messages.push({ sender: 'Bot', text: response.response });
          this.query = ''; // Clear the input field
        },
        error => {
          console.error('Error querying PDF', error);
        }
      );
    }
  }

  changePdf() {
    this.router.navigate(['/upload']);
  }

  private extractFileName(filePath: string): string {
    // Extract the file name from the file path
    const parts = filePath.split(/[\\/]/); // Split by both forward and backward slashes
    return parts.pop() || ''; // Return the file name or an empty string if extraction fails
  }
}
