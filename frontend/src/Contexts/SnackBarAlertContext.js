import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { useState, createContext} from 'react';

export const SnackbarContext = createContext({});

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}


const SnackBarContextProvider = ({children}) => {

    /*
        Serverity levels
        "error"
        "warning"
        "info"
        "success"
    */
    const [snackbar, setSnackbar] = useState({
        message: '',
        severity: '',
        open: false,
      });
  
    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setSnackbar({...snackbar, open: false});
    };

    return (
    <SnackbarContext.Provider value={{ snackbar, setSnackbar }}>
        {children}
        <div>
            <Snackbar open={snackbar.open} autoHideDuration={9000} onClose={handleClose}>
                <div>
                    <Alert onClose={handleClose} severity={snackbar.severity}>
                        {snackbar.message}
                    </Alert>
                </div>
            </Snackbar>
        </div>
    </SnackbarContext.Provider>
    )
}

export default SnackBarContextProvider