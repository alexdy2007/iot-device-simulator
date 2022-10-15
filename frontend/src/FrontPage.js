import './FrontPage.css';

import NavBar from './Components/Navbar/Navbar'
import DevicePage from './Components/DevicesPage/DevicePage';
import { Fragment } from 'react';

function FrontPage() {


  return (
    <Fragment>
      <NavBar></NavBar>
      <div className="body">
        <DevicePage>

        </DevicePage>
       
      </div>

    </Fragment>
  );
}

export default FrontPage;
