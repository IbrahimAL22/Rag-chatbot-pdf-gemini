import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UploadComponent } from './upload/upload.component';
import { QueryComponent } from './query/query.component';
import { PdfService } from './pdf.service';

@NgModule({
  declarations: [
    AppComponent,
    UploadComponent,
    QueryComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [PdfService],
  bootstrap: [AppComponent]
})
export class AppModule { }
