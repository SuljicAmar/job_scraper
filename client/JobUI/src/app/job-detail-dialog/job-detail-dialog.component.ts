import { Job } from '../models/job.model';
import {ChangeDetectionStrategy, Component, Inject} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {
  MatDialogRef,
  MatDialogClose,
  MatDialogContent,
  MatDialogActions,
  MAT_DIALOG_DATA
} from '@angular/material/dialog';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-job-detail-dialog',
  styleUrls: ['./job-detail-dialog.component.css'],
  template: `
  <mat-dialog-content>
    <h4>Responsibilities:</h4>
    <ul *ngFor="let responsibility of job.details.responsibilities">
        <li>{{ responsibility }}</li>
    </ul>
    <h4>Requirements:</h4>
    <ul *ngFor="let req of job.details.requirements">
        <li>{{ req }}</li>
    </ul>
    <h4>Skills:</h4>
    <ul *ngFor="let skill of job.details.skills">
        <li>{{ skill }}</li>
    </ul>
</mat-dialog-content>
<mat-dialog-actions align="end">
    <button mat-button mat-dialog-close>Close</button>
    <a [href]="job.url" target="_blank">
        <button mat-button [mat-dialog-close]="true" cdkFocusInitial>Apply</button>
    </a>
</mat-dialog-actions>
`,
  imports: [MatButtonModule, CommonModule, MatDialogContent, MatDialogClose, MatDialogActions],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JobDetailDialogComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public job: Job, // Injecting the Job data
    private dialogRef: MatDialogRef<JobDetailDialogComponent> // Injecting MatDialogRef
  ) {}
  close() {
    // Close the dialog
    this.dialogRef.close();
  }

}
