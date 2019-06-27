import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer';
import UserForm from '../components/UserForm';


const formData = {
    username: '',
    email: '',
    password: ''
}
describe('When not authenticated', () => {

    test('Registration Form renders without crashing', () => {
        const wrapper = shallow(<UserForm
            type='registration'
            isAuthenticated={false}
            title='Registration Form'
            formData={formData} />);
        const h1 = wrapper.find('h1');
        expect(h1.length).toBe(1);
        expect(h1.get(0).props.children).toBe('Registration Form');
        const formGroup = wrapper.find('.field').find('input');
        expect(formGroup.length).toBe(4);
        expect(formGroup.get(0).props.name).toBe('username');
        expect(formGroup.get(0).props.value).toBe('');
        expect(formGroup.get(0).props.type).toBe('text');
        expect(formGroup.get(1).props.name).toBe('email');
        expect(formGroup.get(1).props.value).toBe('');
        expect(formGroup.get(1).props.type).toBe('text');
        expect(formGroup.get(2).props.name).toBe('password');
        expect(formGroup.get(2).props.value).toBe('');
        expect(formGroup.get(2).props.type).toBe('password');
    });

    test('Login Form renders without crashing', () => {
        const wrapper = shallow(<UserForm
            isAuthenticated={false}
            type='login'
            title='Login Form'
            formData={formData} />);
        const h1 = wrapper.find('h1');
        expect(h1.length).toBe(1);
        expect(h1.get(0).props.children).toBe('Login Form');
        const formGroup = wrapper.find('.field').find('input');
        expect(formGroup.length).toBe(3);
        expect(formGroup.get(0).props.name).toBe('username');
        expect(formGroup.get(0).props.value).toBe('');
        expect(formGroup.get(0).props.type).toBe('text');
        expect(formGroup.get(1).props.name).toBe('password');
        expect(formGroup.get(1).props.value).toBe('');
        expect(formGroup.get(1).props.type).toBe('password');
    });

    test('Registration snapshot matches properly', () => {
        const tree = renderer.create(
            <UserForm type='registration'
                isAuthenticated={false}
                title='Registration Form'
                formData={formData} />).toJSON()
        expect(tree).toMatchSnapshot();
    });

    test('Login snapshot matches properly', () => {
        const tree = renderer.create(
            <UserForm
                type='login'
                isAuthenticated={false}
                title='Login Form'
                formData={formData} />).toJSON()
        expect(tree).toMatchSnapshot();
    });

    it('Registraction Forms call submit properly', () => {
        const handleSubmit = jest.fn();
        const handleChange = jest.fn();

        const wrapper = shallow(<UserForm
            type='registration'
            isAuthenticated={false}
            title='Registration Form'
            handleSubmit={handleSubmit}
            handleChange={handleChange}
            formData={formData} />);
        expect(handleSubmit).toHaveBeenCalledTimes(0);
        expect(handleChange).toHaveBeenCalledTimes(0);
        const formGroup = wrapper.find('.field').find('input');
        formGroup.at(0).simulate('change');
        formGroup.at(1).simulate('change');
        formGroup.at(2).simulate('change');
        expect(handleChange).toHaveBeenCalledTimes(3);
        wrapper.find('form').simulate('submit', formData);
        expect(handleSubmit).toHaveBeenCalledWith(formData);
        expect(handleSubmit).toHaveBeenCalledTimes(1);
    })
    it('Login Forms call submit properly', () => {

        const handleSubmit = jest.fn();
        const handleChange = jest.fn();
        const wrapper = shallow(<UserForm
            type='registration'
            isAuthenticated={false}
            title='Registration Form'
            handleSubmit={handleSubmit}
            handleChange={handleChange}
            formData={formData} />);
        expect(handleSubmit).toHaveBeenCalledTimes(0);
        expect(handleChange).toHaveBeenCalledTimes(0);
        const formGroup = wrapper.find('.field').find('input');
        formGroup.at(0).simulate('change');
        formGroup.at(1).simulate('change');
        expect(handleChange).toHaveBeenCalledTimes(2);
        wrapper.find('form').simulate('submit', formData);
        expect(handleSubmit).toHaveBeenCalledWith(formData);
        expect(handleSubmit).toHaveBeenCalledTimes(1);
    })
});

describe('When authenticated', () => {
    test('Login Form redirects to home', () => {
        const wrapper = shallow(<UserForm
            isAuthenticated={true}
            type='login'
            title='Login Form'
            formData={formData} />);
        expect(wrapper.find('Redirect')).toHaveLength(1);
    });

    test('Registration Form redirects to home', () => {
        const wrapper = shallow(<UserForm
            isAuthenticated={true}
            type='registration'
            title='Registration Form'
            formData={formData} />);
        expect(wrapper.find('Redirect')).toHaveLength(1);
    });



})
