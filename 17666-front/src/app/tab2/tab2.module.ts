import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Tab2Page } from './tab2.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

//import { environment } from './environments/environment';
import { environment } from './../../environments/environment';

import { AngularFireModule } from 'angularfire2';
import { AngularFireAuthModule } from 'angularfire2/auth';
import { AngularFireDatabaseModule } from 'angularfire2/database';
import { AngularFirestoreModule } from 'angularfire2/firestore';


import { Tab2PageRoutingModule } from './tab2-routing.module';


@NgModule({
  imports: [
    IonicModule,
    AngularFireModule.initializeApp(environment.firebase), // init
    AngularFireDatabaseModule, // add realtime DB module
    AngularFirestoreModule, // add cloudstore DB module
    AngularFireAuthModule, // add auth module
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    Tab2PageRoutingModule
  ],
  declarations: [Tab2Page]
})
export class Tab2PageModule { }

