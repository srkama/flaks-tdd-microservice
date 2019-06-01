import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer';
import Aboutus from '../components/Aboutus';

it('renders without crashing', () => {
    const wrapper = shallow(<Aboutus />)
    const element = wrapper.find('p')
    expect(element.length).toBe(1);
    expect(element.text()).toBe('About us');
});

test('About us snapshots renders properly', () => {
    const tree = renderer.create(<Aboutus />).toJSON();
    expect(tree).toMatchSnapshot();
})