import { Component } from '@angular/core';
import { JobTableComponent } from './job-table/job-table.component'; // Import your JobTableComponent
import { Job } from './models/job.model'; // Import your Job model
import { CommonModule } from '@angular/common'; // Required for standalone components
import { ApiService } from './services/api.service'; // Import your service for fetching jobs
import { MatTableDataSource } from '@angular/material/table';  // Import MatTableDataSource

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
     <!-- Pass MatTableDataSource to JobTableComponent -->
  `,
  imports: [CommonModule, JobTableComponent],
  styleUrls: ['./app.component.css'],
  templateUrl: './app.component.html',
})
export class AppComponent {
  jobData = new MatTableDataSource<Job>();  // Initialize as MatTableDataSource

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Fetch job data from the API when the component initializes
    this.apiService.getJobs().subscribe({
      next: (data) => {
        this.jobData.data = data; // Assign fetched job data to MatTableDataSource's data property
      },
      error: (err) => {
        console.error('Error fetching jobs:', err);
      },
    });
  }
}