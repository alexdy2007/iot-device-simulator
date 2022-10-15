import './FrontPage.css';

import NavBar from './Components/Navbar/Navbar'
import DevicePage from './Components/DevicesPage/DevicePage';
import { Fragment } from 'react';
import SnackBarContextProvider from './Contexts/SnackBarAlertContext'


function FrontPage() {


  return (
    <Fragment>
      <NavBar></NavBar>
      <div className="body">
        <SnackBarContextProvider>
          <DevicePage>

          </DevicePage>
        </SnackBarContextProvider>

       
      </div>

    </Fragment>
  );
}

export default FrontPage;
