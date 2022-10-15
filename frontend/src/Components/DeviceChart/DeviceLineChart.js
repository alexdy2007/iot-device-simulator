import { Fragment } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

import moment from 'moment';

const DeviceLineChart = (props) => {
    let deviceData = props.deviceData
    let deviceMetric = props.deviceMetric

    return (
        <Fragment>
            <ResponsiveContainer width='95%' height={200} >
                <LineChart
                    width={500}
                    height={300}
                    data={deviceData}
                    margin={{
                        top: 5,
                        right: 10,
                        left: 0,
                        bottom: 5,
                    }}
                >
                    <XAxis domain={['dataMin', 'dataMax']} scale='time' type='number' tickFormatter={(unixtime) => moment.unix(unixtime).format('HH:mm:ss')} dataKey="unixtime" />
                    <YAxis type='number' domain={[dataMin => (Math.floor(dataMin, 0)), dataMax => (Math.ceil(dataMax, 0))]} />
                    <Line animationDuration={50} type="monotone" dataKey="value" stroke="#82ca9d" />
                    <Tooltip labelFormatter={(value) => {return `time: ${moment.unix(value).format('HH:mm:ss')}`;}} />
                    <CartesianGrid strokeDasharray="3 3" />
                </LineChart>
            </ResponsiveContainer>
        </Fragment>
    );

}

export default DeviceLineChart
