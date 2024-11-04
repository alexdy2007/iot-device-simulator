import './FrontPage.css';

import NavBar from './Components/Navbar/Navbar'
import DevicePage from './Components/DevicesPage/DevicePage';
import DeviceDashboard from './Components/Dashboards/DeviceDashboard';
import { Fragment } from 'react';
import SnackBarContextProvider from './Contexts/SnackBarAlertContext'
import { BrowserRouter, Routes, Route } from "react-router-dom";


function FrontPage() {


  return (
    <Fragment>
      <div className="body">
          <SnackBarContextProvider>
          <BrowserRouter>
          <NavBar></NavBar>

            <Routes>
                <Route path='/' element={<DevicePage />} />
                <Route path="dashboard" element={<DeviceDashboard />} />
            </Routes>
        </BrowserRouter>
        </SnackBarContextProvider>
    </div>

    </Fragment>
  );
}

export default FrontPage;
