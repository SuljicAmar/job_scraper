import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { ApiService } from '../services/api.service';
import { Job } from '../models/job.model';
import { JobDetailDialogComponent } from '../job-detail-dialog/job-detail-dialog.component';

@Component({
  selector: 'app-job-table',
  standalone: true,
  template: `
<mat-form-field >
    <mat-label>Filter</mat-label>
    <input matInput (keyup)="applyFilter($event)" placeholder="Search" #input>
</mat-form-field>

<table mat-table [dataSource]="dataSource" matSort>

    <ng-container matColumnDef="job_title">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Title </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.job_title }} </td>
    </ng-container>

    <ng-container matColumnDef="company_name">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Company </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.company_name }} </td>
    </ng-container>

    <ng-container matColumnDef="location">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Location </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.location }} </td>
    </ng-container>

    <ng-container matColumnDef="job_type">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Type </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.job_type }} </td>
    </ng-container>

    <ng-container matColumnDef="min_salary">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Min Salary </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.minimum_salary | number: '1.0' }} </td>
    </ng-container>

    <ng-container matColumnDef="max_salary">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Max Salary </th>
        <td mat-cell *matCellDef="let job"> {{ job.details.maximum_salary | number: '1.0' }} </td>
    </ng-container>

    <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
    <tr mat-row *matRowDef="let row; columns: displayedColumns;" (click)="openDialog(row)"></tr>
</table>
<mat-paginator [pageSize]="5" [pageSizeOptions]="[5, 10, 20]" showFirstLastButtons></mat-paginator>
`,
  styleUrls: ['./job-table.component.css'],
  imports: [CommonModule,
    MatTableModule,
    MatPaginatorModule,
    MatFormFieldModule,
    MatSortModule,
    MatInputModule,
    MatButtonModule,
    MatDialogModule],
})
export class JobTableComponent implements OnInit {
  displayedColumns: string[] = ['job_title', 'company_name', 'location', 'job_type', 'min_salary', 'max_salary'];
  @Input() dataSource: MatTableDataSource<Job> = new MatTableDataSource<Job>(); // Initialize MatTableDataSource
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private apiService: ApiService, private dialog: MatDialog) { }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  openDialog(row: Job): void {
    // Open the dialog and pass the selected row to it
    this.dialog.open(JobDetailDialogComponent, {
      data: row,  // Pass the selected row data to the dialog
    });
  }

  ngOnInit(): void {
    this.apiService.getJobs().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;

        this.dataSource.sortingDataAccessor = (item, property) => {
          switch (property) {
            case 'job_title': return item.details.job_title;
            case 'company_name': return item.details.company_name;
            case 'location': return item.details.location;
            case 'job_type': return item.details.job_type;
            case 'min_salary': return item.details.minimum_salary;
            case 'max_salary': return item.details.maximum_salary;
            default: return '';
          }
        };
      },
      error: (err) => {
        console.error('Error fetching jobs:', err);
      },
    });

    // Set filter predicate for the search bar
    this.dataSource.filterPredicate = (data: Job, filter: string) => {
      const filterValue = filter.toLowerCase();
      return data.details.job_title.toLowerCase().includes(filterValue) ||
        data.details.company_name.toLowerCase().includes(filterValue) ||
        data.details.job_type.toLowerCase().includes(filterValue) ||
        data.details.responsibilities.map((data: string) => data.toLowerCase()).includes(filterValue) ||
        data.details.requirements.map((data: string) => data.toLowerCase()).includes(filterValue) ||
        data.details.skills.map((data: string) => data.toLowerCase()).includes(filterValue);
    };
  }
}