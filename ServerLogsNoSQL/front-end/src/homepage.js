import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

export default class Home extends React.Component {

    componentDidMount() {

        fetch('/api/welcome', {
            headers: {
                'Accept': 'application/json',
            },
            method: 'GET'
         })
        .then(response => response.json())
        .then(response => {
            console.log(response);
        });
    }

    render() {
        return(
            <Container>
                <Row>
                    <Col>
                        <h1> Welcome to Log DB! </h1>
                    </Col>
                </Row>
            </Container>
        );
    }
}