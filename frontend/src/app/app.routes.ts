import { Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { QueryComponent } from './query/query.component';

export const appRoutes: Routes = [
  { path: '', redirectTo: '/upload', pathMatch: 'full' },
  { path: 'upload', component: UploadComponent },
  { path: 'chat', component: QueryComponent }
];
