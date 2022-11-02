import { CategoryResponse } from './Module/categoryResponse';
import { AfterViewInit, Component, OnInit } from '@angular/core';
import { BackendServiceService } from '../service/backend-service.service';

import { AngularFireDatabase } from 'angularfire2/database';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit{
  testText: string;
  bean: any;
  items$: Observable<any[]>;
  response: any[];
  filter: any[];
  selectValue: any;
  selectOptions: any[];
  constructor(private db: AngularFireDatabase, private backendServiceService: BackendServiceService) {
  }
  async ngOnInit(): Promise<void> {
    this.items$ = this.db.list('items').valueChanges();
    this.items$.subscribe({
      next: result => {
        this.response = result;
      }
    });
    // this.backendServiceService.testApi().subscribe({
    //   next: result => {
    //     console.log(result);
    //     this.testText = result.text;
    //   }
    // });
  }

  optionOnChange(event: any): void {
    this.filter = [];
    // console.log(event);
    console.log(event);
    console.log('hello World');
    for (const row of this.response) {
      if (row.category.toString() === event) {
        this.filter.push(row);
      }
    }
  }

}
