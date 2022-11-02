import { BackendServiceService } from './../service/backend-service.service';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AngularFireDatabase } from 'angularfire2/database';
import { ToggleCustomEvent } from '@ionic/angular';

@Component({
  selector: 'app-tab4',
  templateUrl: './tab4.page.html',
  styleUrls: ['./tab4.page.scss'],
})
export class Tab4Page implements OnInit {

  searchString: string;
  testText: string;
  bean: any;
  items$: Observable<any[]>;
  response: any[];
  selectValue: any;
  selectOptions: any[];
  request: any = {question: ''};
  predictAns: any;
  finalAns: any[] = [];

  constructor(private db: AngularFireDatabase, private backendServiceService: BackendServiceService) {
    this.searchString = '';
   }

  ngOnInit() {
    this.items$ = this.db.list('tab4').valueChanges();
    this.items$.subscribe({
      next: result => {
        this.response = result;
      }
    });
  }

  enterKeyIn() {
    this.finalAns = [];
    console.log(this.searchString);
    this.request.question = this.searchString;
    this.backendServiceService.predict(this.request).subscribe({
      next: result => {
        const predictAnsJson = result;
        this.predictAns = JSON.parse(predictAnsJson);
        console.log(this.predictAns);
        for (const predict of this.predictAns) {
          for (const row of this.response) {
            if (row.idx.toString() === predict.idx) {
              const filterRow = row;
              console.log(filterRow);
              filterRow.likely = parseFloat(predict.likely);
              console.log(filterRow.likely);
              this.finalAns.push(filterRow);
            }
          }
        }
        console.log(this.finalAns);
      }
    });
  }

}
