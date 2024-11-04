import { Fragment, useState, useEffect, useRef } from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from "@mui/material/Box";


const DeviceDashboard = (props) => {

    const [loading, setLoading] = useState(true);


    return (
        <Fragment>
            <div>Dashboard</div>
            { loading ? 
            
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="100vh"
            >
                <CircularProgress size={90} color="secondary" /> 
            </Box>: <></> }

            <iframe 
            src="https://e2-demo-field-eng.cloud.databricks.com/embed/dashboardsv3/01ef8c8317711d46a99f285694ec97ad?o=1444828305810485" 
            width="100%" height="1000" frameborder="0"
            onLoad={() => setLoading(false)}></iframe>
        </Fragment>
    )

}

export default DeviceDashboard;