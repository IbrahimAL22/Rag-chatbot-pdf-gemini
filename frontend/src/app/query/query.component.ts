import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PdfService } from '../pdf.service';

@Component({
  selector: 'app-query',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.scss'],
  providers: [PdfService]
})
export class QueryComponent {
  query: string = '';
  messages: { sender: string, text: string }[] = [];

  constructor(private pdfService: PdfService) { }

  sendQuery() {
    const filePath = localStorage.getItem('pdfFilePath');
    if (filePath && this.query) {
      this.pdfService.queryPdf(filePath, this.query).subscribe(
        response => {
          this.messages.push({ sender: 'User', text: this.query });
          this.messages.push({ sender: 'Bot', text: response.response });
          this.query = '';
        },
        error => {
          console.error('Error querying PDF', error);
        }
      );
    }
  }
}
