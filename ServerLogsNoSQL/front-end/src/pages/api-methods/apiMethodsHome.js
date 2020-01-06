import React from 'react';

import { Container, Row, Col, Button, Card } from 'react-bootstrap';

export default class ApiMethods extends React.Component {

    render() {
        return (
            <Container className="navbar-margin text-center">
                <Row>
                    <Col>
                        <Card>
                            <Card.Header as="h3" className="text-center bg-dark" style={{color:'white'}}> Choose the API method to execute. </Card.Header>

                            <Card.Body>
                                <Row>
                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/1')} }
                                        >
                                            <b> Method 1 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/2')} }
                                        >
                                            <b> Method 2 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/3')} }
                                        >
                                            <b> Method 3 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/4')} }
                                        >
                                            <b> Method 4 </b>
                                        </Button>
                                    </Col>
                                </Row>

                                <Row>
                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/5')} }
                                        >
                                            <b> Method 5 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/6')} }
                                        >
                                            <b> Method 6 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/7')} }
                                        >
                                            <b> Method 7 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/8')} }
                                        >
                                            <b> Method 8 </b>
                                        </Button>
                                    </Col>
                                </Row>

                                <Row>
                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/9')} }
                                        >
                                            <b> Method 9 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/10')} }
                                        >
                                            <b> Method 10 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                        <Button
                                            size="lg"
                                            block
                                            style={{height: '150px', marginBottom: '5px', marginTop: '5px'}}
                                            variant="dark"
                                            onClick={ () => {this.props.history.push('/api-methods/11')} }
                                        >
                                            <b> Method 11 </b>
                                        </Button>
                                    </Col>

                                    <Col>
                                    
                                    </Col>
                                </Row>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        );
    }
}