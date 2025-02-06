import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router'; // Import RouterModule

import { AppComponent } from './app.component';
import { UploadComponent } from './upload/upload.component';
import { QueryComponent } from './query/query.component';
import { NavbarComponent } from './navbar/navbar.component'; // Import NavbarComponent
import { PdfService } from './pdf.service';
import { appRoutes } from './app.routes'; // Import appRoutes

@NgModule({
  declarations: [
    AppComponent,
    UploadComponent,
    QueryComponent,
    NavbarComponent // Declare NavbarComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    
    RouterModule.forRoot(appRoutes) // Use appRoutes for routing
  ],
  providers: [PdfService],
  bootstrap: [AppComponent]
})
export class AppModule { }
